#!/usr/bin/env python3
import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
EXCLUDE_DIRS = {"ai-skills-index", "ai-skills-browser", "SkillsBrowser.app"}

def parse_skill_md(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    frontmatter = {}
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            yaml_content = content[3:end].strip()
            for line in yaml_content.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip().strip('"')
    return frontmatter

def get_all_skills():
    skills = []
    for item in os.listdir(SKILL_DIR):
        item_path = os.path.join(SKILL_DIR, item)
        if os.path.isdir(item_path) and item not in EXCLUDE_DIRS:
            md_path = os.path.join(item_path, "SKILL.md")
            if os.path.exists(md_path):
                skill_info = parse_skill_md(md_path)
                if skill_info:
                    skill_info["id"] = item
                    skill_info["name"] = skill_info.get("name", item)
                    skills.append(skill_info)
    return skills

def get_skill_detail(skill_id):
    md_path = os.path.join(SKILL_DIR, skill_id, "SKILL.md")
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.split("\n")
        frontmatter = {}
        body_lines = []
        if content.startswith("---"):
            frontmatter_end = -1
            for i, line in enumerate(lines):
                if i == 0: continue
                if line.strip() == "---":
                    frontmatter_end = i
                    break
            if frontmatter_end > 0:
                for i in range(1, frontmatter_end):
                    line = lines[i]
                    if ":" in line:
                        key, value = line.split(":", 1)
                        value = value.strip().strip('"').strip("'")
                        frontmatter[key.strip()] = value
                for i in range(frontmatter_end + 1, len(lines)):
                    body_lines.append(lines[i])
        else:
            body_lines = lines[1:] if len(lines) > 1 else []
        return {"frontmatter": frontmatter, "content": "\n".join(body_lines).strip()}
    return None

class Handler(SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/skills":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(get_all_skills()).encode())
            return
        if parsed.path.startswith("/api/skill/"):
            skill_id = parsed.path[11:]
            detail = get_skill_detail(skill_id)
            if detail:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(detail).encode())
            else:
                self.send_response(404)
                self.end_headers()
            return
        if parsed.path == "/" or parsed.path == "/index.html":
            html_path = os.path.join(SCRIPT_DIR, "index.html")
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html_content.encode())
            else:
                self.send_response(404)
                self.end_headers()
            return
        super().do_GET()

def main():
    port = 8765
    import webbrowser
    webbrowser.open(f"http://localhost:{port}/")
    server = HTTPServer(("0.0.0.0", port), Handler)
    print("Skills Browser: http://127.0.0.1:" + str(port))
    server.serve_forever()

if __name__ == "__main__":
    main()
