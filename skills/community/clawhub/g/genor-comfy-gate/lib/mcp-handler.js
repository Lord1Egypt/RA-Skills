/**
 * MCP (Model Context Protocol) handler for Genor-Comfy-Gate
 *
 * Implements streamable-http transport per MCP spec:
 *   POST /mcp  — tools/list, tools/call, resources/list, resources/read
 *
 * This makes the gateway fully LLM-compatible so any AI assistant
 * can discover workflows, understand their parameters, and generate.
 */

import crypto from 'crypto';
import { execSync } from 'child_process';
import { listWorkflowsMeta, getWorkflow, loadWorkflowJson, previewSchema, applyParamsToWorkflow, saveWorkflowJsonFile, createWorkflow } from './workflow-registry.js';
import { SERVERS } from './load-balancer.js';
import { submitPrompt } from './comfy-proxy.js';
import { waitForPrompt, findOutputInHistory, downloadAndSave, listMedia, oneTimeTokens, newToken, trackPrompt, updatePromptStatus, getGenerationStatus } from './media-manager.js';
import path from 'path';
import fs from 'fs';
import { MEDIA_DIR, contentTypeForFile } from './media-manager.js';

const GATEWAY_PUBLIC_BASE = (process.env.GATEWAY_PUBLIC_URL || `http://localhost:${process.env.PORT || '8188'}`).replace(/\/$/, '');

function buildAccessUrl(token) {
  return `${GATEWAY_PUBLIC_BASE}/media-once/${token}`;
}

function issueOneTimeAccessUrl(savedFile) {
  const subpath = path.relative(MEDIA_DIR, savedFile);
  const token = newToken();
  const tokenDuration = 365 * 24 * 60 * 60 * 1000;
  oneTimeTokens.set(token, { subpath, expiresAt: Date.now() + tokenDuration });
  return buildAccessUrl(token);
}

// ─── Tools ───────────────────────────────────────────────────────

const MCP_TOOLS = [
  {
    name: 'list_workflows',
    description: 'List all registered ComfyUI workflows with their type (audio/image), format (mp3/png), editable params, and description. Use this first to discover available capabilities.',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'get_workflow_details',
    description: 'Get detailed info about a specific workflow including its editable parameters (prompt, lyrics, duration, bpm, keyscale, seed, aspect_ratio), output type, and preview/schema for interactive param editing.',
    inputSchema: {
      type: 'object',
      properties: {
        workflow_id: {
          type: 'string',
          description: 'Workflow ID (e.g. acestep-aio, ). Use list_workflows to see all available.',
        },
      },
      required: ['workflow_id'],
    },
  },
  {
    name: 'generate',
    description: 'Run a ComfyUI generation. Default mode sync blocks until complete and returns file_url + access_url (one-time token link). mode=auto submits async — returns prompt_id; poll check_generation for status. For audio: prompt, lyrics, duration, bpm, keyscale. For images: prompt, aspect_ratio.',
    inputSchema: {
      type: 'object',
      properties: {
        workflow: {
          type: 'string',
          description: 'Workflow ID to use (e.g. acestep-aio)',
        },
        params: {
          type: 'object',
          description: 'Generation parameters. For acestep-aio: { prompt, lyrics?, duration?, bpm?, keyscale?, language? }.',
          properties: {
            prompt: { type: 'string', description: 'Tags/prompt for the generation' },
            lyrics: { type: 'string', description: 'Lyrics with [section] markers (audio only)' },
            duration: { type: 'number', description: 'Song duration in seconds (audio only)' },
            bpm: { type: 'number', description: 'Beats per minute (audio only)' },
            keyscale: { type: 'string', description: 'Key and scale, e.g. E minor (audio only)' },
            language: { type: 'string', description: 'Language code, e.g. en (audio only)' },
            model_sampling: { type: 'boolean', description: 'Enable ModelSamplingAuraFlow (shift=13). Default false (bypassed). Only applies to acestep-aio.' },
            aspect_ratio: { type: 'string', description: 'Aspect ratio for image, e.g. 896x1152 (image only)' },
          },
        },
        seed: {
          type: 'number',
          description: 'Random seed (-1 for random)',
          default: -1,
        },
        mode: {
          type: 'string',
          enum: ['sync', 'auto'],
          description: 'sync (default): block until done, return access_url. auto: submit async, return prompt_id.',
          default: 'sync',
        },
      },
      required: ['workflow', 'params'],
    },
  },
  {
    name: 'check_generation',
    description: 'Check the status of a submitted generation by prompt_id. Returns current status (submitted/running/completed/failed/timeout), file_path if completed, and queue info.',
    inputSchema: {
      type: 'object',
      properties: {
        prompt_id: {
          type: 'string',
          description: 'The upstream_prompt_id or gateway prompt_id returned from generate()',
        },
      },
      required: ['prompt_id'],
    },
  },
  {
    name: 'generate_raw',
    description: 'Submit an ad-hoc custom ComfyUI workflow JSON directly. Use this for experimental workflows not in the registry, or for one-off generations with custom node configurations. Returns the output file path and metadata.',
    inputSchema: {
      type: 'object',
      properties: {
        workflow: {
          type: 'object',
          description: 'Full ComfyUI workflow JSON object. Must have proper node structure with inputs, class_type, etc.',
        },
        output_filename: {
          type: 'string',
          description: 'Optional custom filename prefix for the output',
        },
      },
      required: ['workflow'],
    },
  },
  {
    name: 'list_media',
    description: 'List generated media files. Filter by type (audio/image), search query, or limit.',
    inputSchema: {
      type: 'object',
      properties: {
        type: {
          type: 'string',
          enum: ['audio', 'image'],
          description: 'Filter by media type',
        },
        q: {
          type: 'string',
          description: 'Search query for filename matching',
        },
        limit: {
          type: 'number',
          description: 'Maximum number of results',
          default: 20,
        },
      },
    },
  },
  {
    name: 'get_workflow_preview_form',
    description: 'Get the interactive form schema for a workflow, including all editable params with their types, labels, defaults, and whether they are required. Useful for building UI forms or knowing exactly what parameters can be injected.',
    inputSchema: {
      type: 'object',
      properties: {
        workflow_id: {
          type: 'string',
          description: 'Workflow ID to get preview form for',
        },
      },
      required: ['workflow_id'],
    },
  },
  {
    name: 'get_health',
    description: 'Get backend server health: online/offline status, circuit breaker state, queue depth (running/pending), VRAM usage for each GPU server (pri = RTX 3090 24GB, sec = RTX 3080 Laptop 16GB). Use this to check if generation servers are available.',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'restart',
    description: 'Restart the gateway via PM2. The gateway will go offline briefly and automatically restart. Use this if the gateway becomes unresponsive or you need to reload configuration.',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'upload_workflow',
    description: 'Upload a new ComfyUI workflow JSON and register it as a reusable workflow. The workflow will be saved to the workflows/ directory and registered in the gateway for future use.',
    inputSchema: {
      type: 'object',
      properties: {
        workflow_id: {
          type: 'string',
          description: 'Unique ID for the workflow (e.g. my-custom-workflow)',
        },
        json_content: {
          type: 'object',
          description: 'The ComfyUI workflow JSON object',
        },
        title: {
          type: 'string',
          description: 'Optional display title for the workflow',
        },
        description: {
          type: 'string',
          description: 'Optional description of what the workflow does',
        },
        type: {
          type: 'string',
          description: 'Media type: audio or image',
          enum: ['audio', 'image'],
        },
        ext: {
          type: 'string',
          description: 'Output file extension (e.g. mp3, png)',
        },
      },
      required: ['workflow_id', 'json_content'],
    },
  },
];

// ─── Resources ───────────────────────────────────────────────────

const MCP_RESOURCES = [
  {
    uri: 'gateway://workflows',
    name: 'All Workflows',
    description: 'List of all registered ComfyUI workflows with metadata',
    mimeType: 'application/json',
  },
  {
    uri: 'gateway://health',
    name: 'Gateway Health',
    description: 'Backend server health and queue status',
    mimeType: 'application/json',
  },
];

// ─── Tool Handlers ───────────────────────────────────────────────

async function handleToolCall(name, args) {
  switch (name) {
    case 'list_workflows': {
      const meta = listWorkflowsMeta();
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(meta, null, 2),
            mimeType: 'application/json',
          },
        ],
      };
    }

    case 'get_workflow_details': {
      const wf = getWorkflow(args.workflow_id);
      if (!wf) {
        return {
          isError: true,
          content: [{ type: 'text', text: `Workflow '${args.workflow_id}' not found. Available: ${Object.keys(listWorkflowsMeta()).join(', ')}` }],
        };
      }
      // Include preview schema in the same call
      let preview = null;
      try { preview = previewSchema(args.workflow_id); } catch {}
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ ...wf, preview }, null, 2),
            mimeType: 'application/json',
          },
        ],
      };
    }

    case 'generate': {
      const { workflow, params = {}, seed, client_id, mode = 'sync' } = args;
      const meta = getWorkflow(workflow);
      if (!meta) {
        const available = Object.keys(listWorkflowsMeta()).join(', ');
        return {
          isError: true,
          content: [{ type: 'text', text: `Unknown workflow: '${workflow}'. Available: ${available}` }],
        };
      }

      const fullParams = { ...params };
      if (seed !== undefined) fullParams.seed = seed;

      // Validate required: prompt
      if (!fullParams.prompt) {
        return {
          isError: true,
          content: [{ type: 'text', text: 'params.prompt is required' }],
        };
      }

      let wfJson;
      try {
        wfJson = loadWorkflowJson(workflow);
        if (!wfJson) throw new Error(`Workflow file not found for: ${workflow}`);
        applyParamsToWorkflow(wfJson, meta, fullParams);
      } catch (e) {
        return {
          isError: true,
          content: [{ type: 'text', text: `Workflow setup error: ${e.message}` }],
        };
      }

      const submitResult = await submitPrompt(SERVERS, {
        prompt: wfJson,
        client_id: client_id || crypto.randomUUID(),
      });

      if (submitResult.status !== 200) {
        return {
          isError: true,
          content: [{ type: 'text', text: `Submit failed (${submitResult.status}): ${JSON.stringify(submitResult.data)}` }],
        };
      }

      const { data } = submitResult;
      const serverId = data.server;
      const upstreamPromptId = data.upstream_prompt_id;
      const gatewayPromptId = data.prompt_id;

      trackPrompt(upstreamPromptId, {
        prompt_type: meta?.type || 'image',
        server_id: serverId,
        server_prompt_id: upstreamPromptId,
        gateway_prompt_id: gatewayPromptId,
        workflow,
        output_node_ids: meta?.output_node_ids || [],
        params: fullParams,
      });

      if (mode === 'auto') {
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                status: 'submitted',
                prompt_id: gatewayPromptId,
                upstream_prompt_id: upstreamPromptId,
                server: serverId,
                workflow,
                check_url: `/health?prompt_id=${gatewayPromptId}`,
                file_url: null,
              }, null, 2),
              mimeType: 'application/json',
            },
          ],
        };
      }

      // sync (default): generate-and-wait — same flow as POST /generate-and-wait
      const server = SERVERS.find((s) => s.id === serverId);
      if (!server) {
        return {
          isError: true,
          content: [{ type: 'text', text: `Server '${serverId}' not found in active pool` }],
        };
      }

      const waitResult = await waitForPrompt(server.url, upstreamPromptId, 600000);
      if (!waitResult.done) {
        updatePromptStatus(upstreamPromptId, 'timeout', { terminal_since: Date.now() });
        return {
          isError: true,
          content: [{ type: 'text', text: `Generation timed out: ${waitResult.error || 'timeout'}` }],
        };
      }
      if (waitResult.status !== 'completed') {
        updatePromptStatus(upstreamPromptId, waitResult.status || 'failed', { terminal_since: Date.now() });
        return {
          isError: true,
          content: [{ type: 'text', text: `Generation failed: ${waitResult.error || waitResult.status}` }],
        };
      }

      await new Promise((r) => setTimeout(r, 3000));
      const output = findOutputInHistory(waitResult.data?.outputs, meta.output_node_ids);
      if (!output) {
        updatePromptStatus(upstreamPromptId, 'failed', { terminal_since: Date.now() });
        return {
          isError: true,
          content: [{ type: 'text', text: 'Generation completed but no output file found in results' }],
        };
      }

      try {
        const saved = await downloadAndSave({
          serverUrl: server.url,
          output,
          workflowId: workflow,
          workflowType: meta.type,
          ext: meta.ext,
          meta: {
            prompt: fullParams.prompt,
            lyrics: fullParams.lyrics || '',
            seed: fullParams.seed || 0,
            aspect_ratio: fullParams.aspect_ratio || '',
            duration: fullParams.duration || 0,
            bpm: fullParams.bpm || 0,
            server: serverId,
            server_prompt_id: upstreamPromptId,
            model: meta.description,
          },
        });

        const accessUrl = issueOneTimeAccessUrl(saved.file);

        updatePromptStatus(upstreamPromptId, 'completed', {
          file_url: saved.url,
          file_path: saved.file,
          terminal_since: Date.now(),
        });

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                status: 'ok',
                file_url: saved.url,
                access_url: accessUrl,
                file_path: saved.file,
                filename: saved.filename,
                server: serverId,
                workflow,
                prompt_id: gatewayPromptId,
                upstream_prompt_id: upstreamPromptId,
                file_size: saved.file_size,
                type: saved.type,
              }, null, 2),
              mimeType: 'application/json',
            },
          ],
        };
      } catch (e) {
        updatePromptStatus(upstreamPromptId, 'failed', { terminal_since: Date.now() });
        return {
          isError: true,
          content: [{ type: 'text', text: `Download/save failed: ${e.message}` }],
        };
      }
    }

    case 'check_generation': {
      const status = getGenerationStatus(args.prompt_id);
      if (!status) {
        return {
          isError: true,
          content: [{ type: 'text', text: `Unknown prompt_id: '${args.prompt_id}'. Not found in gateway queue.` }],
        };
      }
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(status, null, 2),
          mimeType: 'application/json',
        }],
      };
    }

    case 'generate_raw': {
      const { workflow: rawWf, output_filename: outName, client_id: rawCid } = args;
      if (!rawWf || typeof rawWf !== 'object') {
        return {
          isError: true,
          content: [{ type: 'text', text: 'workflow must be a valid ComfyUI workflow JSON object' }],
        };
      }

      const subResult = await submitPrompt(SERVERS, {
        prompt: rawWf,
        client_id: rawCid || crypto.randomUUID(),
      });

      if (subResult.status !== 200) {
        return {
          isError: true,
          content: [{ type: 'text', text: `Submit failed: ${JSON.stringify(subResult.data)}` }],
        };
      }

      // Track raw prompt
      const rawPromptId = subResult.data.upstream_prompt_id;
      trackPrompt(rawPromptId, {
        prompt_type: 'image',
        server_id: subResult.data.server,
        server_prompt_id: rawPromptId,
        workflow: outName || 'raw',
        params: {},
      });

      // Always wait for completion (mode removed — always blocking)

      const rServer = SERVERS.find((s) => s.id === subResult.data.server);
      const rPid = subResult.data.upstream_prompt_id;
      const rWait = await waitForPrompt(rServer.url, rPid, 600000);

      if (!rWait.done || rWait.status !== 'completed') {
        return {
          isError: true,
          content: [{ type: 'text', text: `Raw generation failed: ${rWait.error || rWait.status || 'timeout'}` }],
        };
      }

      await new Promise((r) => setTimeout(r, 3000));
      const rOut = findOutputInHistory(rWait.data?.outputs);
      if (!rOut) {
        return {
          isError: true,
          content: [{ type: 'text', text: 'Raw generation completed but no output found' }],
        };
      }

      const ext = (rOut.filename || '').split('.').pop() || 'bin';
      const wfType = rOut.mediaKind === 'audio' ? 'audio' : 'image';
      try {
        const saved = await downloadAndSave({
          serverUrl: rServer.url,
          output: rOut,
          workflowId: outName || 'raw',
          workflowType: wfType,
          ext,
        });

        updatePromptStatus(rawPromptId, 'completed', {
          file_url: saved.url,
          file_path: saved.file,
          terminal_since: Date.now(),
        });

        const accessUrl = issueOneTimeAccessUrl(saved.file);

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              status: 'ok',
              ...saved,
              file_url: saved.url,
              access_url: accessUrl,
              file_path: saved.file,
            }, null, 2),
            mimeType: 'application/json',
          }],
        };
      } catch (e) {
        return {
          isError: true,
          content: [{ type: 'text', text: `Download failed: ${e.message}` }],
        };
      }
    }

    case 'list_media': {
      const media = listMedia({ type: args.type, q: args.q, limit: args.limit || 20 });
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(media, null, 2),
          mimeType: 'application/json',
        }],
      };
    }

    case 'get_workflow_preview_form': {
      const schema = previewSchema(args.workflow_id);
      if (!schema) {
        return {
          isError: true,
          content: [{ type: 'text', text: `Workflow '${args.workflow_id}' not found or has no preview schema` }],
        };
      }
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(schema, null, 2),
          mimeType: 'application/json',
        }],
      };
    }

    case 'get_health': {
      const { getServerHealth } = await import('./load-balancer.js');
      const servers = await getServerHealth();
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({ servers }, null, 2),
          mimeType: 'application/json',
        }],
      };
    }

    case 'restart': {
      try {
        execSync('sleep 2 && pm2 restart genor-comfy-gate', { stdio: 'ignore' });
        return {
          content: [{ type: 'text', text: 'Gateway restart initiated. It will be back online in a few seconds.' }],
        };
      } catch (e) {
        return {
          isError: true,
          content: [{ type: 'text', text: `Restart failed: ${e.message}` }],
        };
      }
    }

    case 'upload_workflow': {
      const { workflow_id, json_content, title, description, type, ext } = args;
      if (!workflow_id || !json_content) {
        return {
          isError: true,
          content: [{ type: 'text', text: 'workflow_id and json_content are required' }],
        };
      }

      try {
        // Create workflow entry in registry FIRST
        const workflowEntry = {
          id: workflow_id,
          title: title || workflow_id.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
          description: description || `Custom workflow uploaded via MCP`,
          type: type || 'other',
          file: `${workflow_id}.json`,
          ext: ext || 'png',
          editable_params: [],
          output_node_ids: [],
          submit_config: {
            client_id_generation: 'auto',
            preserve_seed: true,
            validation_schema: {},
          },
        };
        
        const created = createWorkflow(workflowEntry);
        
        // NOW save the workflow JSON file (registry entry exists)
        saveWorkflowJsonFile(workflow_id, json_content);
        
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ ok: true, workflow: created }, null, 2),
            mimeType: 'application/json',
          }],
        };
      } catch (e) {
        return {
          isError: true,
          content: [{ type: 'text', text: `Upload failed: ${e.message}` }],
        };
      }
    }

    default:
      return {
        isError: true,
        content: [{ type: 'text', text: `Unknown tool: ${name}` }],
      };
  }
}

// ─── MCP Router (Express middleware) ─────────────────────────────

export function mcpRouter(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed', jsonrpc: '2.0' });
  }

  const body = req.body;

  // Support both single request and batch
  const requests = Array.isArray(body) ? body : [body];

  Promise.all(
    requests.map(async (rpc) => {
      const { id, method, params } = rpc;

      // Validate JSON-RPC
      if (rpc.jsonrpc !== '2.0' || !method) {
        return { jsonrpc: '2.0', id: id || null, error: { code: -32600, message: 'Invalid Request' } };
      }

      switch (method) {
        case 'initialize': {
          return {
            jsonrpc: '2.0',
            id,
            result: {
              protocolVersion: '2025-03-26',
              capabilities: {
                tools: {},
                resources: {},
                roots: { listChanged: false },
              },
              serverInfo: {
                name: 'genor-comfy-gate',
                version: '2.0',
              },
            },
          };
        }

        case 'ping': {
          return { jsonrpc: '2.0', id, result: {} };
        }

        case 'tools/list': {
          return {
            jsonrpc: '2.0',
            id,
            result: { tools: MCP_TOOLS },
          };
        }

        case 'tools/call': {
          try {
            const result = await handleToolCall(params.name, params.arguments || {});
            return { jsonrpc: '2.0', id, result };
          } catch (e) {
            return {
              jsonrpc: '2.0',
              id,
              error: { code: -32603, message: `Internal error: ${e.message}` },
            };
          }
        }

        case 'resources/list': {
          return {
            jsonrpc: '2.0',
            id,
            result: { resources: MCP_RESOURCES },
          };
        }

        case 'resources/read': {
          const uri = params?.uri;
          if (uri === 'gateway://workflows') {
            return {
              jsonrpc: '2.0',
              id,
              result: {
                contents: [{
                  uri: 'gateway://workflows',
                  mimeType: 'application/json',
                  text: JSON.stringify(listWorkflowsMeta(), null, 2),
                }],
              },
            };
          }

          if (uri === 'gateway://health') {
            const { getServerHealth } = await import('./load-balancer.js');
            const servers = await getServerHealth();
            return {
              jsonrpc: '2.0',
              id,
              result: {
                contents: [{
                  uri: 'gateway://health',
                  mimeType: 'application/json',
                  text: JSON.stringify({ servers }, null, 2),
                }],
              },
            };
          }

          // Maybe a media file
          if (uri?.startsWith('gateway://media/')) {
            const subpath = uri.slice('gateway://media/'.length);
            const fullPath = path.join(MEDIA_DIR, subpath);
            if (fs.existsSync(fullPath)) {
              const mime = contentTypeForFile(fullPath);
              const data = fs.readFileSync(fullPath).toString('base64');
              return {
                jsonrpc: '2.0',
                id,
                result: {
                  contents: [{
                    uri,
                    mimeType: mime,
                    blob: data,
                  }],
                },
              };
            }
            return {
              jsonrpc: '2.0',
              id,
              error: { code: -32602, message: `Resource not found: ${uri}` },
            };
          }

          return {
            jsonrpc: '2.0',
            id,
            error: { code: -32602, message: `Unknown resource: ${uri}` },
          };
        }

        case 'notifications/initialized':
        case 'notifications/cancelled':
          // No response needed per MCP spec
          return null;

        default:
          return {
            jsonrpc: '2.0',
            id,
            error: { code: -32601, message: `Method not found: ${method}` },
          };
      }
    }),
  ).then((responses) => {
    const filtered = responses.filter((r) => r !== null);
    if (filtered.length === 0) {
      return res.status(202).end();
    }
    if (Array.isArray(body)) {
      return res.json(filtered);
    }
    return res.json(filtered[0]);
  }).catch((e) => {
    console.error('MCP handler error:', e);
    if (Array.isArray(body)) {
      return res.status(500).json([{ jsonrpc: '2.0', id: null, error: { code: -32603, message: 'Internal error' } }]);
    }
    return res.status(500).json({ jsonrpc: '2.0', id: null, error: { code: -32603, message: 'Internal error' } });
  });
}
