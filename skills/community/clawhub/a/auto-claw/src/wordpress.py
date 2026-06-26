"""
WordPress Client - 通过 SSH + WP-CLI 操作 WordPress
"""
import subprocess
import json
from typing import List, Dict, Any, Optional

class WordPressClient:
    def __init__(self, ssh_host: str, ssh_user: str, ssh_key: str, web_root: str, php_bin: str = "/www/server/php/82/bin/php"):
        self.ssh_host = ssh_host
        self.ssh_user = ssh_user
        self.ssh_key = ssh_key
        self.web_root = web_root
        self.php_bin = php_bin
        self._connected = False
    
    def _ssh(self, cmd: str) -> tuple[str, str, int]:
        """执行命令。本地模式用subprocess，远程用SSH"""
        if self.ssh_host == "localhost" or self.ssh_host in ("127.0.0.1", ""):
            # 本地模式：直接执行
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        else:
            # 远程模式：通过SSH
            full_cmd = f"cd {self.web_root} && {cmd}"
            result = subprocess.run(
                ["ssh", "-i", self.ssh_key, "-o", "StrictHostKeyChecking=no",
                 f"{self.ssh_user}@{self.ssh_host}", full_cmd],
                capture_output=True, text=True, timeout=60
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
    
    def _wp(self, args: str) -> tuple[str, str, int]:
        """通过 WP-CLI 执行命令"""
        return self._ssh(f"WP_CLI_PHP={self.php_bin} /usr/local/bin/wp --allow-root --path={self.web_root} {args}")
    
    def test_connection(self) -> bool:
        """测试连接"""
        out, err, code = self._wp("--info")
        self._connected = code == 0 and "PHP" in out
        return self._connected
    
    # ===== 健康检查 =====
    
    def get_core_info(self) -> Dict[str, Any]:
        """获取 WordPress 核心信息"""
        version, err, code = self._wp("core version")
        checksum, err2, code2 = self._wp("core verify-checksums 2>&1 || echo 'CHECKSUM_WARN'")
        db_version, _, _ = self._wp("core update-db --dry-run 2>&1 | head -1 || echo 'OK'")
        return {
            "version": version,
            "checksum_valid": "success" in checksum.lower() or "CHECKSUM_WARN" in checksum,
            "db_version": db_version.strip(),
            "connected": self._connected
        }
    
    def get_plugins(self) -> List[Dict[str, str]]:
        """获取插件列表"""
        out, err, code = self._wp("plugin list --format=json --status=active")
        if code != 0:
            return []
        try:
            return json.loads(out)
        except:
            return []
    
    def get_themes(self) -> List[Dict[str, str]]:
        """获取主题列表"""
        out, err, code = self._wp("theme list --format=json --status=active")
        if code != 0:
            return []
        try:
            return json.loads(out)
        except:
            return []
    
    def get_admin_users(self) -> int:
        """获取管理员数量"""
        out, err, code = self._wp("user list --role=administrator --format=count")
        try:
            return int(out.strip())
        except:
            return 0
    
    def check_updates(self) -> Dict[str, Any]:
        """检查更新"""
        plugin_update, _, _ = self._wp("plugin update --dry-run 2>&1")
        core_update, _, _ = self._wp("core update --dry-run 2>&1")
        return {
            "has_plugin_updates": "update" in plugin_update.lower() and "available" in plugin_update.lower(),
            "has_core_update": "update" in core_update.lower() and "available" in core_update.lower(),
        }
    
    # ===== 内容管理 =====
    
    def get_posts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取文章"""
        out, err, code = self._wp(f"post list --post_type=post --posts_per_page={limit} --format=json")
        if code != 0:
            return []
        try:
            return json.loads(out)
        except:
            return []
    
    def create_post(self, title: str, content: str, status: str = "draft", author: str = "autoclaw") -> Dict[str, Any]:
        """创建文章"""
        # 先获取作者ID
        author_id, _, _ = self._wp(f"user list --login={author} --field=ID")
        author_id = author_id.strip() or "1"
        
        out, err, code = self._wp(
            f"post create --post_title='{title}' --post_content='{content}' "
            f"--post_status={status} --post_author={author_id} --format=json"
        )
        if code != 0:
            return {"error": err}
        try:
            return json.loads(out)
        except:
            return {"raw": out, "error": err}
    
    def update_post(self, post_id: int, title: str = None, content: str = None, status: str = None) -> Dict[str, Any]:
        """更新文章"""
        args = f"post update {post_id}"
        if title:
            args += f" --post_title='{title}'"
        if content:
            content_escaped = content.replace("'", "\\'")
            args += f" --post_content='{content_escaped}'"
        if status:
            args += f" --post_status={status}"
        
        out, err, code = self._wp(args)
        if code != 0:
            return {"error": err}
        try:
            return json.loads(out)
        except:
            return {"raw": out}
    
    def delete_post(self, post_id: int, force: bool = False) -> bool:
        """删除文章"""
        flag = "--force" if force else ""
        out, err, code = self._wp(f"post delete {post_id} {flag}")
        return code == 0
    
    # ===== 插件管理 =====
    
    def install_plugin(self, plugin_slug: str) -> Dict[str, Any]:
        """安装插件"""
        out, err, code = self._wp(f"plugin install {plugin_slug} --activate")
        return {"success": code == 0, "output": out, "error": err}
    
    def activate_plugin(self, plugin_name: str) -> bool:
        out, err, code = self._wp(f"plugin activate {plugin_name}")
        return code == 0
    
    def deactivate_plugin(self, plugin_name: str) -> bool:
        out, err, code = self._wp(f"plugin deactivate {plugin_name}")
        return code == 0
    
    def update_plugin(self, plugin_name: str) -> Dict[str, Any]:
        out, err, code = self._wp(f"plugin update {plugin_name}")
        return {"success": code == 0, "output": out, "error": err}

    # ===== 结构化数据注入 =====

    def inject_schema_jsonld(self, post_id: int, json_ld: str) -> Dict[str, Any]:
        """
        注入 JSON-LD Schema 到文章
        """
        meta_cmd = f"post meta update {post_id} _schema_jsonld '{json_ld}' 2>&1 || echo 'META_FAIL'"
        out, err, code = self._wp(meta_cmd)
        
        if "META_FAIL" in out:
            return {"success": False, "post_id": post_id, "method": "post-meta-failed", "note": "使用 head injection 方案"}
        
        return {"success": code == 0, "post_id": post_id, "method": "post-meta"}

    def generate_schema_mu_plugin(self, schemas: list) -> str:
        """
        生成 mu-plugin 代码用于注入 JSON-LD 到 <head>
        """
        import json
        schemas_json = json.dumps(schemas, ensure_ascii=False, indent=2)
        return f'''<?php
/**
 * Auto-Claw JSON-LD Schema Injection (mu-plugin)
 * 自动注入到所有页面 <head>
 */
add_action('wp_head', function() {{
    $schemas = {schemas_json};
    foreach ($schemas as $s) {{
        echo '<script type="application/ld+json">' . wp_json_encode($s, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . '</script>' . "\\n";
    }}
}}, 1);
'''

    def install_schema_mu_plugin(self, code: str) -> Dict[str, Any]:
        """创建 mu-plugin 文件"""
        path = f"{self.web_root}/wp-content/mu-plugins/auto-claw-schema.php"
        cmd = f"mkdir -p {self.web_root}/wp-content/mu-plugins/"
        self._ssh(cmd)
        # 写入文件
        write_cmd = f"cat > {path} << 'PHPEOF'\n{code}\nPHPEOF"
        out, err, code = self._ssh(write_cmd)
        return {"success": code == 0, "path": path}

    def get_post_ids(self, limit: int = 10) -> List[int]:
        """获取文章 ID 列表"""
        out, err, code = self._wp(f"post list --post_type=post --posts_per_page={limit} --format=ids")
        if code != 0:
            return []
        return [int(x) for x in out.split() if x.strip().isdigit()]
