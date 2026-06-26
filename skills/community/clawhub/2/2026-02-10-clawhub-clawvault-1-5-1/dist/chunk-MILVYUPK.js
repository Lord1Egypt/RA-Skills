import {
  checkDirtyDeath,
  clearDirtyFlag
} from "./chunk-MZZJLQNQ.js";
import {
  formatAge
} from "./chunk-7ZRP733D.js";

// src/commands/recover.ts
import * as fs from "fs";
import * as path from "path";
async function recover(vaultPath, options = {}) {
  const { clearFlag = false } = options;
  const { died, checkpoint, deathTime } = await checkDirtyDeath(vaultPath);
  if (!died) {
    return {
      died: false,
      deathTime: null,
      checkpoint: null,
      handoffPath: null,
      handoffContent: null,
      recoveryMessage: "No context death detected. Clean startup."
    };
  }
  const handoffsDir = path.join(vaultPath, "handoffs");
  let handoffPath = null;
  let handoffContent = null;
  if (fs.existsSync(handoffsDir)) {
    const files = fs.readdirSync(handoffsDir).filter((f) => f.startsWith("handoff-") && f.endsWith(".md")).sort().reverse();
    if (files.length > 0) {
      handoffPath = path.join(handoffsDir, files[0]);
      handoffContent = fs.readFileSync(handoffPath, "utf-8");
    }
  }
  let message = "\u26A0\uFE0F **CONTEXT DEATH DETECTED**\n\n";
  message += `Your previous session died at ${deathTime}.

`;
  if (checkpoint) {
    message += "**Last known state:**\n";
    if (checkpoint.workingOn) {
      message += `- Working on: ${checkpoint.workingOn}
`;
    }
    if (checkpoint.focus) {
      message += `- Focus: ${checkpoint.focus}
`;
    }
    if (checkpoint.blocked) {
      message += `- Blocked: ${checkpoint.blocked}
`;
    }
    message += "\n";
  }
  if (handoffPath) {
    message += `**Last handoff:** ${path.basename(handoffPath)}
`;
    message += "Review and resume from where you left off.\n";
  } else {
    message += "**No handoff found.** You may have lost context.\n";
  }
  if (clearFlag) {
    await clearDirtyFlag(vaultPath);
  }
  return {
    died: true,
    deathTime,
    checkpoint,
    handoffPath,
    handoffContent,
    recoveryMessage: message
  };
}
function formatRecoveryInfo(info, options = {}) {
  const { verbose = false } = options;
  if (!info.died) {
    return "\u2713 Clean startup - no context death detected.";
  }
  let output = "\n\u26A0\uFE0F  CONTEXT DEATH DETECTED\n";
  output += "\u2550".repeat(40) + "\n\n";
  output += `Death time: ${info.deathTime}
`;
  if (info.checkpoint?.timestamp) {
    const age = formatAge(Date.now() - new Date(info.checkpoint.timestamp).getTime());
    output += `Checkpoint: ${info.checkpoint.timestamp} (${age} ago)
`;
  }
  output += "\n";
  if (info.checkpoint) {
    output += "Last checkpoint:\n";
    if (info.checkpoint.workingOn) {
      output += `  \u2022 Working on: ${info.checkpoint.workingOn}
`;
    }
    if (info.checkpoint.focus) {
      output += `  \u2022 Focus: ${info.checkpoint.focus}
`;
    }
    if (info.checkpoint.blocked) {
      output += `  \u2022 Blocked: ${info.checkpoint.blocked}
`;
    }
    if (info.checkpoint.sessionKey || info.checkpoint.model || info.checkpoint.tokenEstimate !== void 0) {
      output += "  \u2022 Session:\n";
      if (info.checkpoint.sessionKey) {
        output += `    - Key: ${info.checkpoint.sessionKey}
`;
      }
      if (info.checkpoint.model) {
        output += `    - Model: ${info.checkpoint.model}
`;
      }
      if (info.checkpoint.tokenEstimate !== void 0) {
        output += `    - Token estimate: ${info.checkpoint.tokenEstimate}
`;
      }
    }
    output += "\n";
  } else {
    output += "No checkpoint data found.\n\n";
  }
  if (info.handoffPath) {
    output += `Last handoff: ${path.basename(info.handoffPath)}
`;
  } else {
    output += "No handoff found - context may be lost.\n";
  }
  if (verbose) {
    if (info.checkpoint) {
      output += "\nCheckpoint JSON:\n";
      output += JSON.stringify(info.checkpoint, null, 2) + "\n";
    }
    if (info.handoffContent) {
      output += "\nHandoff content:\n";
      output += info.handoffContent.trim() + "\n";
    }
  }
  output += "\n" + "\u2550".repeat(40) + "\n";
  output += "Run `clawvault recap` to see full context.\n";
  return output;
}

export {
  recover,
  formatRecoveryInfo
};
