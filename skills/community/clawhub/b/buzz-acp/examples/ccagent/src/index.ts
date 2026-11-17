#!/usr/bin/env node
import { Readable, Writable } from "node:stream";
import { AgentSideConnection, ndJsonStream } from "@zed-industries/agent-client-protocol";
import { ZaphoidAgent, AGENT_NAME } from "./agent.js";

process.stderr.write(`${AGENT_NAME} ACP agent starting on stdio...\n`);

const stream = ndJsonStream(
  Writable.toWeb(process.stdout) as WritableStream<Uint8Array>,
  Readable.toWeb(process.stdin) as ReadableStream<Uint8Array>,
);

new AgentSideConnection((conn) => new ZaphoidAgent(conn), stream);
