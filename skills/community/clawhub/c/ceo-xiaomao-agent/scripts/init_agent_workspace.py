#!/usr/bin/env python3
import os
from pathlib import Path

WORKDIR = Path(os.environ.get('CEO_XIAOMAO_WORKDIR', os.getcwd()))

files = {
    'SOUL.md': '# SOUL.md\n\n请从 references/SOUL.md 复制并按需调整。\n',
    'USER.md': '# USER.md\n\n- **Name:** [老板姓名]\n- **What to call them:** 老板\n- **Timezone:** Asia/Shanghai\n- **Role:** 外贸B2B业务负责人\n',
    'MEMORY.md': '# MEMORY.md\n\n## 当前业务\n\n## 当前团队\n\n## 当前待办\n',
    'AGENTS.md': '# AGENTS.md\n\n每次启动按顺序读取：SOUL.md → USER.md → MEMORY.md → 当天 memory 文件。\n',
    'IDENTITY.md': '# IDENTITY.md\n\n- **Name:** CEO小茂（小茂）\n- **Role:** AI团队协调总控 / CEO助理\n',
}

dirs = ['tasks', 'docs', 'leads', 'crm', 'attachments', 'memory']

for d in dirs:
    (WORKDIR / d).mkdir(parents=True, exist_ok=True)

for name, content in files.items():
    path = WORKDIR / name
    if not path.exists():
        path.write_text(content, encoding='utf-8')
        print(f'created {path}')
    else:
        print(f'exists {path}')

print('workspace ready:', WORKDIR)
