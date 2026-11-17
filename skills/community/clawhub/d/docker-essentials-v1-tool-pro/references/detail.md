# 详细参考 - docker-essentials-v1-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import os
import re
import json
from datetime import datetime

class CompatibilityScanner:
    """V1到V2兼容性深度扫描器"""

    def __init__(self, project_root):
        self.project_root = project_root
        self.issues = []
        self.warnings = []
        self.suggestions = []

    def scan_all(self):
        """执行完整扫描"""
        self._scan_compose_files()
        self._scan_dockerfiles()
        self._scan_scripts()
        self._scan_ci_cd()
        return self._generate_report()

    def _scan_compose_files(self):
        """扫描Compose文件"""
        compose_patterns = [
            "docker-compose*.yml",
            "docker-compose*.yaml",
            "compose*.yml"
        ]

        for pattern in compose_patterns:
            for root, _, files in os.walk(self.project_root):
                for f in files:
                    if re.match(pattern.replace('*', '.*'), f):
                        filepath = os.path.join(root, f)
                        self._analyze_compose_file(filepath)

    def _analyze_compose_file(self, filepath):
        """分析单个Compose文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        version_match = re.search(r'^version:\s*["\']?(\d+\.?\d*)["\']?', content, re.M)
        if version_match:
            version = version_match.group(1)
            if version in ['1', '2']:
                self.warnings.append({
                    "file": filepath,
                    "issue": f"Compose版本 {version} 建议升级到 3.8",
                    "severity": "warning",
                    "auto_fix": True
                })

        deprecated = {
            r"^\s*links:": "links特性已弃用,V2使用网络别名替代",
            r"^\s*external_links:": "external_links已弃用",
            r"container_name:": "不建议硬编码容器名,影响扩展",
            r"^\s*volumes_from:": "volumes_from已弃用,使用命名卷替代",
        }

        for pattern, message in deprecated.items():
            if re.search(pattern, content, re.M):
                self.issues.append({
                    "file": filepath,
                    "issue": message,
                    "severity": "high",
                    "auto_fix": True
                })

    def _scan_dockerfiles(self):
        """扫描Dockerfile"""
        for root, _, files in os.walk(self.project_root):
            for f in files:
                if f.startswith('Dockerfile'):
                    filepath = os.path.join(root, f)
                    self._analyze_dockerfile(filepath)

    def _analyze_dockerfile(self, filepath):
        """分析Dockerfile"""
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if stripped.startswith('MAINTAINER'):
                self.issues.append({
                    "file": filepath,
                    "line": i,
                    "issue": "MAINTAINER已弃用,使用LABEL maintainer替代",
                    "severity": "medium",
                    "auto_fix": True,
                    "original": stripped,
                    "suggestion": f'LABEL maintainer="{stripped.split(" ", 1)[1]}"'
                })

            if stripped.startswith('FROM ') and ' AS ' not in stripped:
                if i == 1 and any('RUN apt' in l or 'RUN yum' in l for l in lines):
                    self.suggestions.append({
                        "file": filepath,
                        "issue": "建议使用多阶段构建减小镜像体积",
                        "severity": "info"
                    })

    def _scan_scripts(self):
        """扫描脚本中的docker命令"""
        script_extensions = ['.sh', '.bash', '.bat', '.ps1']

        for root, _, files in os.walk(self.project_root):
            for f in files:
                if any(f.endswith(ext) for ext in script_extensions):
                    filepath = os.path.join(root, f)
                    self._analyze_script(filepath)

    def _analyze_script(self, filepath):
        """分析脚本"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if 'docker-compose' in content and 'docker compose' not in content:
            self.warnings.append({
                "file": filepath,
                "issue": "使用docker-compose(V1),建议迁移到docker compose(V2)",
                "severity": "warning",
                "auto_fix": True
            })

    def _scan_ci_cd(self):
        """扫描CI/CD配置"""
        ci_patterns = ['.gitlab-ci.yml', '.github/workflows/*.yml', 'Jenkinsfile']

        for pattern in ci_patterns:
            for root, _, files in os.walk(self.project_root):
                for f in files:
                    if f in pattern or pattern.endswith(f):
                        filepath = os.path.join(root, f)
                        self._analyze_ci_file(filepath)

    def _analyze_ci_file(self, filepath):
        """分析CI配置"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if 'docker-compose' in content:
            self.warnings.append({
                "file": filepath,
                "issue": "CI配置使用docker-compose V1,需更新为docker compose V2",
                "severity": "high",
                "auto_fix": True
            })

    def _generate_report(self):
        """生成迁移评估报告"""
        return {
            "scan_time": datetime.now().isoformat(),
            "project": self.project_root,
            "summary": {
                "total_issues": len(self.issues),
                "total_warnings": len(self.warnings),
                "total_suggestions": len(self.suggestions),
                "auto_fixable": sum(1 for i in self.issues if i.get("auto_fix")) +
                               sum(1 for w in self.warnings if w.get("auto_fix"))
            },
            "issues": self.issues,
            "warnings": self.warnings,
            "suggestions": self.suggestions,
            "migration_readiness": self._assess_readiness()
        }

    def _assess_readiness(self):
        """评估迁移就绪度"""
        critical = sum(1 for i in self.issues if i["severity"] == "high")
        if critical == 0 and len(self.warnings) < 5:
            return {"ready": True, "level": "高", "estimated_effort": "1-2天"}
        elif critical < 5:
            return {"ready": True, "level": "中", "estimated_effort": "3-5天"}
        else:
            return {"ready": False, "level": "低", "estimated_effort": "1-2周"}

scanner = CompatibilityScanner("./")
report = scanner.scan_all()
print(json.dumps(report, indent=2, ensure_ascii=False))
```

## 代码示例 (bash)

```bash
#!/bin/bash
echo "=== 渐进式迁移管理 ==="

MIGRATION_STATE=".migration-state.json"

init_migration() {
    cat > "$MIGRATION_STATE" << 'EOF'
{
    "started_at": "$(date -Iseconds)",
    "phase": "assessment",
    "services": {},
    "rollback_points": []
}
EOF
    echo "迁移状态已初始化"
}

create_rollback_point() {
    local service="$1"
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local backup_dir="backups/$service-$timestamp"

    mkdir -p "$backup_dir"

    cp -r docker-compose*.yml "$backup_dir/" 2>/dev/null
    cp -r Dockerfile* "$backup_dir/" 2>/dev/null
    cp -r .env* "$backup_dir/" 2>/dev/null

    python3 -c "
import json
with open('$MIGRATION_STATE', 'r') as f:
    state = json.load(f)
state['rollback_points'].append({
    'service': '$service',
    'timestamp': '$timestamp',
    'backup_dir': '$backup_dir'
})
with open('$MIGRATION_STATE', 'w') as f:
    json.dump(state, f, indent=2)
"
    echo "回滚点已创建: $backup_dir"
}

rollback_service() {
    local service="$1"

    BACKUP=$(python3 -c "
import json
with open('$MIGRATION_STATE', 'r') as f:
    state = json.load(f)
points = [p for p in state['rollback_points'] if p['service'] == '$service']
if points:
    print(points[-1]['backup_dir'])
")

    if [ -n "$BACKUP" ] && [ -d "$BACKUP" ]; then
        echo "回滚 $service 到: $BACKUP"
        cp -r "$BACKUP"/* .
        echo "回滚完成"
    else
        echo "未找到 $service 的回滚点"
    fi
}

migrate_service() {
    local service="$1"
    echo "=== 迁移服务: $service ==="

    create_rollback_point "$service"

    echo "停止V1服务..."
    docker-compose stop "$service" 2>/dev/null

    echo "转换配置..."
    echo "使用V2启动..."
    docker compose up -d "$service"

    echo "验证服务..."
    sleep 5
    if docker compose ps "$service" | grep -q "Up"; then
        echo "[OK] $service 迁移成功"
    else
        echo "[FAIL] $service 迁移失败,执行回滚"
        rollback_service "$service"
        docker-compose up -d "$service"
    fi
}
```

## 代码示例 (bash)

```bash
#!/bin/bash
echo "=== 批量配置转换 ==="

convert_compose_file() {
    local file="$1"
    local backup="${file}.v1-backup"

    echo "转换: $file"
    cp "$file" "$backup"

    sed -i 's/^version:.*/version: "3.8"/' "$file"

    sed -i '/^\s*links:/,/^\s*[^-]/{/links:/d; /^\s*-/d}' "$file"

    sed -i '/^\s*external_links:/,/^\s*[^-]/{/external_links:/d; /^\s*-/d}' "$file"

    sed -i '/^\s*volumes_from:/d' "$file"

    echo "  -> 备份: $backup"
    echo "  -> 转换完成"
}

find . -name "docker-compose*.yml" -o -name "docker-compose*.yaml" | while read f; do
    convert_compose_file "$f"
done

convert_dockerfile() {
    local file="$1"
    local backup="${file}.v1-backup"

    echo "转换: $file"
    cp "$file" "$backup"

    sed -i 's/^MAINTAINER \(.*\)/LABEL maintainer="\1"/' "$file"

    echo "  -> 备份: $backup"
    echo "  -> 转换完成"
}

find . -name "Dockerfile*" | while read f; do
    convert_dockerfile "$f"
done

convert_scripts() {
    local file="$1"

    echo "转换脚本: $file"
    sed -i 's/docker-compose /docker compose /g' "$file"

    echo "  -> 命令已更新"
}

find . -name "*.sh" -o -name "*.bash" | while read f; do
    if grep -q "docker-compose" "$f"; then
        convert_scripts "$f"
    fi
done

echo -e "\n=== 转换完成 ==="
echo "所有V1配置已转换为V2格式"
echo "原始文件备份为 .v1-backup"
```

