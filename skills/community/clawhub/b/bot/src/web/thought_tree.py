import json
import html
from http.server import BaseHTTPRequestHandler, HTTPServer

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>BOT Thought Tree</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; padding: 24px; background: #0b1020; color: #e5e7eb; }
    .wrap { max-width: 1180px; margin: 0 auto; }
    .hero { background: linear-gradient(135deg, #111827, #172554); border: 1px solid #243056; border-radius: 20px; padding: 24px; margin-bottom: 18px; box-shadow: 0 8px 24px rgba(0,0,0,0.25); }
    .hero h1 { margin: 0 0 8px 0; font-size: 32px; }
    .muted { color: #94a3b8; }
    .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 18px; }
    .stat { background: #121933; border: 1px solid #243056; border-radius: 16px; padding: 16px; }
    .stat .label { color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; }
    .stat .value { font-size: 24px; font-weight: 700; margin-top: 6px; }
    .card { background: #121933; border: 1px solid #243056; border-radius: 16px; padding: 20px; margin-bottom: 18px; box-shadow: 0 8px 24px rgba(0,0,0,0.25); }
    h2, h3 { margin-top: 0; }
    .node { margin-left: 18px; padding-left: 16px; border-left: 2px solid #334155; margin-top: 14px; }
    .pill { display: inline-block; padding: 4px 10px; border-radius: 999px; background: #1d4ed8; color: white; font-size: 12px; margin-left: 8px; }
    ul { margin-top: 8px; }
    pre { background: #0f172a; border-radius: 10px; padding: 14px; overflow-x: auto; border: 1px solid #243056; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <h1>BOT Monitor</h1>
      <div class="muted">Prompt: __PROMPT__</div>
      <div class="stats">
        <div class="stat">
          <div class="label">Mode</div>
          <div class="value">__MODE__</div>
        </div>
        <div class="stat">
          <div class="label">Agents</div>
          <div class="value">__AGENT_COUNT__</div>
        </div>
        <div class="stat">
          <div class="label">Viewer</div>
          <div class="value">Local</div>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>Tree View</h2>
      __TREE_HTML__
    </div>

    <div class="card">
      <h2>Raw JSON</h2>
      <pre>__RAW_JSON__</pre>
    </div>
  </div>
</body>
</html>
"""

def render_node(node):
    label = html.escape(str(node.get("label", "unknown")))
    confidence = node.get("confidence", None)
    thoughts = node.get("thoughts", [])
    children = node.get("children", [])

    confidence_html = ""
    if confidence is not None:
        confidence_html = f'<span class="pill">confidence: {confidence}</span>'

    thoughts_html = ""
    if thoughts:
        items = "".join(f"<li>{html.escape(str(t))}</li>" for t in thoughts)
        thoughts_html = f"<ul>{items}</ul>"

    children_html = ""
    if children:
        children_html = "".join(render_node(child) for child in children)

    return f'''
    <div class="node">
      <h3>{label}{confidence_html}</h3>
      {thoughts_html}
      {children_html}
    </div>
    '''

class ThoughtTreeHandler(BaseHTTPRequestHandler):
    data = {}

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        prompt = html.escape(str(self.data.get("prompt", "")))
        tree = self.data.get("thought_tree", {})
        agents = self.data.get("agents", [])
        mode = "Multi-Agent" if len(agents) > 1 else "Single-Agent"
        tree_html = render_node(tree) if tree else "<p>No tree data</p>"
        raw_json = html.escape(json.dumps(self.data, indent=2, ensure_ascii=False))

        page_html = (
            HTML_TEMPLATE
            .replace("__PROMPT__", prompt)
            .replace("__MODE__", mode)
            .replace("__AGENT_COUNT__", str(len(agents)))
            .replace("__TREE_HTML__", tree_html)
            .replace("__RAW_JSON__", raw_json)
        )
        page = page_html.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

def serve_thought_tree(data, host="127.0.0.1", port=8765):
    ThoughtTreeHandler.data = data
    server = HTTPServer((host, port), ThoughtTreeHandler)
    print(f"BOT monitor running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()
