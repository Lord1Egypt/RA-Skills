async function handleSoul(body) {
  const message = body.message || "";
  const userId = body.user_id || body.userId || "default";
  const speakerHint = body.speaker || "";
  if (!message) return { error: "message is required" };
  const { generateAvatarReply, loadAvatarProfile } = await import("./avatar.ts");
  const { spawnCLI } = await import("./cli.ts");
  let speaker = speakerHint;
  if (!speaker) {
    const profile = loadAvatarProfile(userId);
    const contacts = Object.entries(profile.social || {}).map(([name, c]) => `${name}\uFF08${c.relation}\uFF09`);
    if (contacts.length > 0) {
      speaker = await new Promise((resolve) => {
        spawnCLI(
          `\u5DF2\u77E5\u5173\u7CFB\uFF1A${contacts.join("\u3001")}
\u6D88\u606F\uFF1A"${message.slice(0, 100)}"
\u6700\u53EF\u80FD\u662F\u8C01\u53D1\u7684\uFF1F\u53EA\u56DE\u7B54\u540D\u5B57\uFF0C\u65E0\u6CD5\u5224\u65AD\u56DE\u7B54"\u672A\u77E5"\u3002`,
          (output) => {
            const name = (output || "").trim().replace(/["""。.，,\s]/g, "");
            if (profile.social[name]) {
              resolve(name);
              return;
            }
            for (const known of Object.keys(profile.social)) {
              if ((output || "").includes(known)) {
                resolve(known);
                return;
              }
            }
            resolve("");
          },
          1e4
        );
      });
    }
  }
  const reply = await new Promise((resolve) => {
    generateAvatarReply(userId, speaker || "\u672A\u77E5", message, (r, refused) => {
      resolve(refused ? "" : r);
    });
  });
  return { reply, speaker: speaker || "\u672A\u77E5" };
}
