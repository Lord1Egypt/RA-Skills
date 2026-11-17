// ============================================================
// DIALOG TREE DATA — maintained by the AI assistant.
// This is the ONLY file to edit per-project; the view
// (dialog-tree.html) is generic and gets replaced on upgrades.
//
// The user's resolve/delete marks live in the browser's
// localStorage keyed by "dialogTree.<treeId>.state.v1" + node
// ids — never change or reuse ids of existing nodes.
//
// who: "user" | "assistant". status: "open" | "resolved"
// (default; the user's localStorage mark overrides it).
// html: template literal — no backticks or ${ inside; escape
// HTML special characters in code samples (&lt; &amp;).
// ============================================================

const META = {
  treeId: "PROJECT-ID",   // unique per project: keys the user's localStorage marks
  builtUpTo: "tree not built yet"
};

const NODES = [
// { id:"t1", parent:null, who:"user", label:"Question…", status:"open", html:`<p>Details…</p>` },
];

// Optional UI localization — uncomment and translate to override the
// view's English defaults (any subset of keys works):
// const STRINGS = {
//   title: "Dialog Tree",
//   builtUpToLabel: "built up to:", showDeleted: "show deleted",
//   placeholder: "Click a node on the left",
//   userName: "🟡 User", assistantName: "🤖 Assistant",
//   resolved: "resolved ✓", open: "open", deleted: "deleted",
//   resolve: "✓ resolve", unresolve: "↩ unresolve",
//   del: "🗑 delete", restore: "↩ restore",
//   counter: (open, total) => `open: ${open} / total: ${total}`,
// };
