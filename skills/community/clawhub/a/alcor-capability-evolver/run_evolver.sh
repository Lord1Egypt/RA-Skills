#!/bin/bash
cd /home/openclaw/.openclaw/workspace_roamer_alcor/skills/alcor-capability-evolver
export A2A_NODE_ID=node_alcor_001
export A2A_NODE_SECRET=e8bc58cff4b0512a43f957bd0750435842146a8925e78d982c379967049c46a8
export A2A_HUB_URL=https://evomap.ai
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
export MEMORY_DIR=/tmp/evolver_memory
node index.js run