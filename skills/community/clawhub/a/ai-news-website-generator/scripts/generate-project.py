#!/usr/bin/env python3
"""
AI资讯网站生成器 - 一键生成完整项目
使用方法: python generate-project.py [项目目录]
"""

import os
import sys
import shutil
from pathlib import Path

# 获取脚本所在目录（Skill目录）
SKILL_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"


def create_project(project_dir: str = "ai-news-website"):
    """生成完整的AI资讯网站项目"""
    
    project_path = Path(project_dir).resolve()
    
    print("=" * 60)
    print("  AI资讯网站生成器")
    print("=" * 60)
    print(f"项目目录: {project_path}")
    print()
    
    # 检查目录是否已存在
    if project_path.exists():
        response = input(f"目录 '{project_path}' 已存在，是否覆盖? (y/N): ")
        if response.lower() != 'y':
            print("已取消")
            return
        shutil.rmtree(project_path)
    
    # 创建目录结构
    print("📁 创建目录结构...")
    (project_path / "frontend" / "app").mkdir(parents=True, exist_ok=True)
    (project_path / "frontend" / "components").mkdir(parents=True, exist_ok=True)
    (project_path / "backend").mkdir(parents=True, exist_ok=True)
    
    # 复制后端文件
    print("🐍 生成后端文件...")
    shutil.copy(TEMPLATES_DIR / "backend-main.py", project_path / "backend" / "main.py")
    shutil.copy(TEMPLATES_DIR / "backend-requirements.txt", project_path / "backend" / "requirements.txt")
    shutil.copy(TEMPLATES_DIR / "backend-Dockerfile", project_path / "backend" / "Dockerfile")
    
    # 复制前端文件
    print("⚛️  生成前端文件...")
    shutil.copy(TEMPLATES_DIR / "frontend-page.tsx", project_path / "frontend" / "app" / "page.tsx")
    shutil.copy(TEMPLATES_DIR / "frontend-package.json", project_path / "frontend" / "package.json")
    shutil.copy(TEMPLATES_DIR / "frontend-Dockerfile", project_path / "frontend" / "Dockerfile")
    shutil.copy(TEMPLATES_DIR / "frontend-next.config.js", project_path / "frontend" / "next.config.js")
    shutil.copy(TEMPLATES_DIR / "frontend-tailwind.config.ts", project_path / "frontend" / "tailwind.config.ts")
    
    # 创建前端布局和样式文件
    (project_path / "frontend" / "app" / "layout.tsx").write_text("""import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI资讯',
  description: '实时聚合全球AI新闻',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  )
}
""")
    
    (project_path / "frontend" / "app" / "globals.css").write_text("""@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #0f172a;
  --foreground: #ffffff;
}

body {
  color: var(--foreground);
  background: var(--background);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
""")
    
    (project_path / "frontend" / "tsconfig.json").write_text("""{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{"name": "next"}],
    "paths": {"@/*": ["./*"]}
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
""")
    
    (project_path / "frontend" / "postcss.config.js").write_text("""module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""")
    
    # 复制根目录文件
    print("📄 生成配置文件...")
    shutil.copy(TEMPLATES_DIR / "docker-compose.yml", project_path / "docker-compose.yml")
    shutil.copy(TEMPLATES_DIR / "README.md", project_path / "README.md")
    shutil.copy(TEMPLATES_DIR / "start.sh", project_path / "start.sh")
    
    # 给脚本加执行权限
    (project_path / "start.sh").chmod(0o755)
    
    print()
    print("=" * 60)
    print("  ✅ 项目生成成功！")
    print("=" * 60)
    print()
    print("下一步:")
    print(f"  cd {project_path}")
    print()
    print("Docker 模式（推荐）:")
    print("  docker-compose up -d --build")
    print()
    print("本地模式:")
    print("  ./start.sh")
    print()
    print("访问地址:")
    print("  前端: http://localhost:3000")
    print("  后端: http://localhost:8000")
    print("  API文档: http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    project_dir = sys.argv[1] if len(sys.argv) > 1 else "ai-news-website"
    create_project(project_dir)
