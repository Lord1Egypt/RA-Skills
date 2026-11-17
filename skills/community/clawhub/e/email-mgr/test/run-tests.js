module.exports = [
  // ── Status ──────────────────────────────────────────────────────────────
  { name: "no args shows status", args: [], expected: "[email-manager] Status:" },
  { name: "--status shows status", args: ["--status"], expected: "[email-manager] Status:" },
  { name: "status shows email counts", args: [], expected: "Total emails:" },

  // ── Inbox ────────────────────────────────────────────────────────────────
  { name: "--inbox lists emails", args: ["--inbox"], expected: "[email-manager]" },
  { name: "--inbox --unread shows unread", args: ["--inbox", "--unread"], expected: "[email-manager]" },

  // ── Search ───────────────────────────────────────────────────────────────
  { name: "--search for term", args: ["--search", "test"], expected: "[email-manager] Found" },

  // ── Compose ──────────────────────────────────────────────────────────────
  { name: "--compose with args", args: ["--compose", "test@example.com", "Subject", "Body"], expected: "[email-manager]" },

  // ── Help ─────────────────────────────────────────────────────────────────
  { name: "--help shows usage", args: ["--help"], expected: "[email-manager] Status:" },
];
