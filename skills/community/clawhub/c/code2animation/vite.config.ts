import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import {defineConfig, loadEnv} from 'vite';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';

const execAsync = promisify(exec);

export default defineConfig(({mode}) => {
  const env = loadEnv(mode, '.', '');
  return {
    plugins: [
      react(), 
      tailwindcss(),
      // Custom plugin to handle API routes
      {
        name: 'audio-api',
        configureServer(server) {
          // API: List all available projects
          server.middlewares.use('/api/projects', async (req, res) => {
            if (req.method !== 'GET') {
              res.statusCode = 405;
              res.end('Method Not Allowed');
              return;
            }

            try {
              const projectsDir = path.resolve(process.cwd(), 'public/projects');
              
              if (!fs.existsSync(projectsDir)) {
                res.setHeader('Content-Type', 'application/json');
                res.end(JSON.stringify({ projects: [] }));
                return;
              }

              const entries = fs.readdirSync(projectsDir, { withFileTypes: true });
              const projectMap = new Map<string, { id: string; name: string; description: string }>();

              // Support top-level format: public/projects/<projectId>.json
              const topLevelJsonFiles = entries.filter(entry => entry.isFile() && entry.name.endsWith('.json'));
              for (const file of topLevelJsonFiles) {
                const projectId = path.basename(file.name, '.json');
                const jsonPath = path.join(projectsDir, file.name);
                try {
                  const projectData = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
                  projectMap.set(projectId, {
                    id: projectId,
                    name: projectData.name || projectId,
                    description: projectData.description || ''
                  });
                } catch (e) {
                  console.error(`Failed to parse ${jsonPath}:`, e);
                }
              }

              // Support nested format: public/projects/<projectId>/<projectId>.json
              const directories = entries.filter(entry => entry.isDirectory() && !entry.name.startsWith('.'));
              for (const entry of directories) {
                const projectId = entry.name;
                const jsonPath = path.join(projectsDir, projectId, `${projectId}.json`);
                if (!fs.existsSync(jsonPath)) continue;

                try {
                  const projectData = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
                  projectMap.set(projectId, {
                    id: projectId,
                    name: projectData.name || projectId,
                    description: projectData.description || ''
                  });
                } catch (e) {
                  console.error(`Failed to parse ${jsonPath}:`, e);
                }
              }

              const projects = Array.from(projectMap.values());

              res.setHeader('Content-Type', 'application/json');
              res.end(JSON.stringify({ projects }));
            } catch (error: any) {
              console.error('[API] Failed to list projects:', error);
              res.statusCode = 500;
              res.setHeader('Content-Type', 'application/json');
              res.end(JSON.stringify({ error: 'Failed to list projects', details: error.message }));
            }
          });

          // API: Generate audio for a project
          server.middlewares.use('/api/generate-audio', async (req, res) => {
            console.log('[API] Received request:', req.method, req.url);
            
            if (req.method !== 'POST') {
              console.log('[API] Method not allowed:', req.method);
              res.statusCode = 405;
              res.end('Method Not Allowed');
              return;
            }

            let body = '';
            req.on('data', chunk => {
              body += chunk.toString();
            });

            req.on('end', async () => {
              try {
                console.log('[API] Request body:', body);
                const { projectId } = JSON.parse(body);
                
                if (!projectId) {
                  console.log('[API] Missing projectId');
                  res.statusCode = 400;
                  res.setHeader('Content-Type', 'application/json');
                  res.end(JSON.stringify({ error: 'projectId is required' }));
                  return;
                }

                console.log(`[API] Starting audio generation for project: ${projectId}`);
                
                // Call the generate-audio script
                const scriptPath = path.resolve(process.cwd(), 'scripts/generate-audio.ts');
                const command = `npx tsx "${scriptPath}" ${projectId}`;
                
                try {
                  const { stdout, stderr } = await execAsync(command);
                  
                  if (stderr) {
                    console.error('[API] Script stderr:', stderr);
                  }
                  
                  console.log('[API] Script stdout:', stdout);
                  console.log('[API] Audio generation completed');
                  
                  res.setHeader('Content-Type', 'application/json');
                  res.end(JSON.stringify({ 
                    success: true, 
                    message: `Audio generation completed for ${projectId}`,
                    output: stdout
                  }));
                } catch (execError: any) {
                  console.error('[API] Script execution failed:', execError);
                  res.statusCode = 500;
                  res.setHeader('Content-Type', 'application/json');
                  res.end(JSON.stringify({ 
                    error: 'Audio generation failed', 
                    details: execError.message,
                    stderr: execError.stderr
                  }));
                }
              } catch (error: any) {
                console.error('[API] Request processing failed:', error);
                res.statusCode = 500;
                res.setHeader('Content-Type', 'application/json');
                res.end(JSON.stringify({ 
                  error: 'Request processing failed', 
                  details: error.message 
                }));
              }
            });
          });
        }
      }
    ],
    define: {
      'process.env.GEMINI_API_KEY': JSON.stringify(env.GEMINI_API_KEY),
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      // HMR is disabled in AI Studio via DISABLE_HMR env var.
      // Do not modifyâfile watching is disabled to prevent flickering during agent edits.
      hmr: process.env.DISABLE_HMR !== 'true',
    },
  };
});
