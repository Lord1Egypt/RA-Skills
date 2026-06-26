#!/bin/bash
# Simple Dialog Template - Single subagent conversation
# Use for: Quick Q&A, simple discussions, single-agent tasks

cat << 'SPAWNPROMPT'
Task: ${TASK_DESCRIPTION}
Target: ${TARGET_DIR}

Spawn 1 teammate using Sonnet:

1. **Dialog Agent**
   - Name: dialog-agent
   - Focus: Answer questions, discuss topics, provide explanations
   - Tasks:
     * Understand the user's request
     * Provide a clear, helpful response
     * If the task requires file operations, read/write as needed

Coordinate the team. When the dialog agent finishes their response, summarize the key points and output exactly CC_CALLBACK_DONE
SPAWNPROMPT
