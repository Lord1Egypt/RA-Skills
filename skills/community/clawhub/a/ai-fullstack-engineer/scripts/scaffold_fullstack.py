#!/usr/bin/env python3
"""scaffold_fullstack.py — 生成可直接运行的全栈应用骨架。

用法:
    python3 scripts/scaffold_fullstack.py --name my-saas --be fastapi --fe react

产物:
    <out>/<name>/
        backend/    FastAPI 或 Express 骨架
        frontend/   React(Vite) 或 Vue(Vite) 骨架
        docker-compose.yaml
        README.md

仅用标准库，无第三方依赖。
"""
import argparse
import os
from pathlib import Path

BE = {"fastapi", "express"}
FE = {"react", "vue"}


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ---------------- 后端骨架 ----------------
def backend_fastapi(root: Path):
    b = root / "backend"
    write(b / "requirements.txt",
          "fastapi\nuvicorn[standard]\npydantic-settings\nsqlalchemy\npython-dotenv\n")
    write(b / "config.py",
          "from pydantic_settings import BaseSettings, SettingsConfigDict\n\n"
          "class Settings(BaseSettings):\n"
          "    model_config = SettingsConfigDict(env_file=\".env\", extra=\"ignore\")\n"
          "    app_name: str = \"my-app\"\n"
          "    database_url: str = \"sqlite+aiosqlite:///./app.db\"\n\n"
          "settings = Settings()\n")
    write(b / "models.py",
          "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column\n\n"
          "class Base(DeclarativeBase):\n    pass\n\n"
          "class User(Base):\n"
          "    __tablename__ = \"users\"\n"
          "    id: Mapped[int] = mapped_column(primary_key=True)\n"
          "    email: Mapped[str] = mapped_column(unique=True)\n")
    write(b / "schemas.py",
          "from pydantic import BaseModel\n\n"
          "class UserCreate(BaseModel):\n    email: str\n\n"
          "class UserOut(BaseModel):\n    id: int\n    email: str\n")
    write(b / "dependencies.py", "from typing import Annotated\nfrom fastapi import Depends\n\n\ndef get_db():\n    yield None  # 替换为真实 DB session\n\n\nDB = Annotated[None, Depends(get_db)]\n")
    write(b / "services.py", "def placeholder() -> str:\n    return \"service layer\"\n")
    write(b / "api/v1/__init__.py", "")
    write(b / "api/v1/users.py",
          "from fastapi import APIRouter\nfrom .. import schemas\n\nrouter = APIRouter(prefix=\"/users\", tags=[\"users\"])\n\n"
          "@router.post(\"\", response_model=schemas.UserOut, status_code=201)\n"
          "def create_user(payload: schemas.UserCreate):\n"
          "    # TODO: 实现创建逻辑\n    return schemas.UserOut(id=1, email=payload.email)\n")
    write(b / "main.py",
          "from contextlib import asynccontextmanager\nfrom fastapi import FastAPI\n"
          "from .api.v1 import users\n\n"
          "@asynccontextmanager\nasync def lifespan(app: FastAPI):\n    yield\n\n"
          "app = FastAPI(lifespan=lifespan)\napp.include_router(users.router)\n\n"
          "if __name__ == \"__main__\":\n"
          "    import uvicorn\n    uvicorn.run(\"main:app\", reload=True)\n")
    write(b / "tests/test_main.py",
          "from fastapi.testclient import TestClient\nfrom main import app\n\n"
          "def test_create_user():\n"
          "    c = TestClient(app)\n"
          "    r = c.post(\"/users\", json={\"email\": \"a@b.com\"})\n"
          "    assert r.status_code == 201\n")


def backend_express(root: Path):
    b = root / "backend"
    write(b / "package.json",
          "{\n  \"name\": \"backend\",\n  \"version\": \"1.0.0\",\n  \"type\": \"module\",\n"
          "  \"scripts\": { \"dev\": \"node --watch src/index.js\", \"start\": \"node src/index.js\" },\n"
          "  \"dependencies\": { \"express\": \"^4.19.2\" }\n}\n")
    write(b / "src/db.js", "export const db = { /* 替换为真实 DB 连接 */ };\n")
    write(b / "src/routes/users.js",
          "import { Router } from \"express\";\nconst router = Router();\n\n"
          "router.post(\"/\", (req, res) => {\n  // TODO: 实现创建逻辑\n  res.status(201).json({ id: 1, email: req.body.email });\n});\n\n"
          "export default router;\n")
    write(b / "src/index.js",
          "import express from \"express\";\nimport users from \"./routes/users.js\";\n\n"
          "const app = express();\napp.use(express.json());\napp.use(\"/users\", users);\n"
          "const port = process.env.PORT || 3000;\napp.listen(port, () => console.log(`API on :${port}`));\n")


# ---------------- 前端骨架 ----------------
FE_CLIENT = (
    "export async function api<T>(path: string, init?: RequestInit): Promise<T> {\n"
    "  const res = await fetch(`/api${path}`, init);\n"
    "  if (!res.ok) throw new Error(`HTTP ${res.status}`);\n"
    "  return res.json() as Promise<T>;\n}\n"
)


def frontend_react(root: Path):
    f = root / "frontend"
    write(f / "package.json",
          "{\n  \"name\": \"frontend\",\n  \"private\": true,\n  \"version\": \"0.0.0\",\n"
          "  \"type\": \"module\",\n  \"scripts\": { \"dev\": \"vite\", \"build\": \"tsc && vite build\", \"preview\": \"vite preview\" },\n"
          "  \"dependencies\": { \"react\": \"^18.3.1\", \"react-dom\": \"^18.3.1\" },\n"
          "  \"devDependencies\": { \"@vitejs/plugin-react\": \"^4.3.1\", \"typescript\": \"^5.5.0\", \"vite\": \"^5.4.0\" }\n}\n")
    write(f / "vite.config.ts",
          "import { defineConfig } from \"vite\";\nimport react from \"@vitejs/plugin-react\";\n\n"
          "export default defineConfig({\n  plugins: [react()],\n  server: { proxy: { \"/api\": \"http://localhost:3000\" } }\n});\n")
    write(f / "tsconfig.json",
          "{ \"compilerOptions\": { \"target\": \"ES2020\", \"module\": \"ESNext\", \"jsx\": \"react-jsx\", \"strict\": true, \"moduleResolution\": \"bundler\", \"noEmit\": true } }\n")
    write(f / "index.html",
          "<!doctype html><html lang=\"zh\"><head><meta charset=\"UTF-8\"/><title>App</title></head>"
          "<body><div id=\"root\"></div><script type=\"module\" src=\"/src/main.tsx\"></script></body></html>\n")
    write(f / "src/main.tsx",
          "import React from \"react\";\nimport { createRoot } from \"react-dom/client\";\nimport App from \"./App\";\n"
          "createRoot(document.getElementById(\"root\")!).render(<App />);\n")
    write(f / "src/api/client.ts", FE_CLIENT)
    write(f / "src/App.tsx",
          "export default function App() {\n  return <h1>Hello Full-Stack</h1>;\n}\n")
    write(f / "src/components/Example.tsx",
          "export function Example({ label }: { label: string }) {\n  return <button>{label}</button>;\n}\n")


def frontend_vue(root: Path):
    f = root / "frontend"
    write(f / "package.json",
          "{\n  \"name\": \"frontend\",\n  \"private\": true,\n  \"version\": \"0.0.0\",\n  \"type\": \"module\",\n"
          "  \"scripts\": { \"dev\": \"vite\", \"build\": \"vite build\", \"preview\": \"vite preview\" },\n"
          "  \"dependencies\": { \"vue\": \"^3.4.0\" },\n  \"devDependencies\": { \"@vitejs/plugin-vue\": \"^5.1.0\", \"vite\": \"^5.4.0\", \"typescript\": \"^5.5.0\" }\n}\n")
    write(f / "vite.config.ts",
          "import { defineConfig } from \"vite\";\nimport vue from \"@vitejs/plugin-vue\";\n\n"
          "export default defineConfig({ plugins: [vue()], server: { proxy: { \"/api\": \"http://localhost:3000\" } } });\n")
    write(f / "tsconfig.json",
          "{ \"compilerOptions\": { \"target\": \"ES2020\", \"module\": \"ESNext\", \"strict\": true, \"moduleResolution\": \"bundler\", \"noEmit\": true, \"jsx\": \"preserve\" } }\n")
    write(f / "index.html",
          "<!doctype html><html lang=\"zh\"><head><meta charset=\"UTF-8\"/><title>App</title></head>"
          "<body><div id=\"app\"></div><script type=\"module\" src=\"/src/main.ts\"></script></body></html>\n")
    write(f / "src/main.ts",
          "import { createApp } from \"vue\";\nimport App from \"./App.vue\";\ncreateApp(App).mount(\"#app\");\n")
    write(f / "src/api/client.ts", FE_CLIENT)
    write(f / "src/App.vue",
          "<script setup lang=\"ts\">\nconst title = \"Hello Full-Stack\";\n</script>\n<template><h1>{{ title }}</h1></template>\n")
    write(f / "src/components/Example.vue",
          "<script setup lang=\"ts\">\ndefineProps<{ label: string }>();\n</script>\n<template><button>{{ label }}</button></template>\n")


def main():
    ap = argparse.ArgumentParser(description="生成全栈应用骨架")
    ap.add_argument("--name", required=True, help="项目名称")
    ap.add_argument("--be", choices=sorted(BE), default="fastapi", help="后端技术栈")
    ap.add_argument("--fe", choices=sorted(FE), default="react", help="前端技术栈")
    ap.add_argument("--out", default=".", help="输出目录（默认当前目录）")
    args = ap.parse_args()

    root = Path(args.out).resolve() / args.name
    if root.exists():
        raise SystemExit(f"目标目录已存在: {root}")
    root.mkdir(parents=True, exist_ok=True)

    if args.be == "fastapi":
        backend_fastapi(root)
    else:
        backend_express(root)

    if args.fe == "react":
        frontend_react(root)
    else:
        frontend_vue(root)

    write(root / "docker-compose.yaml",
          "services:\n"
          "  backend:\n    build: ./backend\n    environment:\n      - PORT=3000\n    ports: [\"3000:3000\"]\n"
          "  frontend:\n    build: ./frontend\n    ports: [\"5173:5173\"]\n")
    write(root / "README.md",
          f"# {args.name}\n\n自动生成的全栈骨架（后端 {args.be} / 前端 {args.fe}）。\n\n"
          "## 本地启动\n\n```bash\n# 后端\ncd backend && (uvicorn main:app --reload  # fastapi)\n"
          "# 前端\ncd frontend && npm install && npm run dev\n```\n\n"
          "契约优先：先定义 `openapi-spec.yaml`，再用 `gen_types_from_openapi.py` 生成前端类型。\n")

    print(f"✓ 已生成 {root}")
    print(f"  后端: {args.be}    前端: {args.fe}")
    print(f"  下一步: cd {args.name} && cat README.md")


if __name__ == "__main__":
    main()
