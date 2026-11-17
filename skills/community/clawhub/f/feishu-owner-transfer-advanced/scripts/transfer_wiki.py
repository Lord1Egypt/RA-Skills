#!/usr/bin/env python3
"""飞书Wiki空间文档所有权批量转移工具。"""
import argparse
import json
import subprocess
import sys


def lark_api(method, path, data=None):
    cmd = ["lark-cli", "api", method, path]
    if data:
        cmd += ["--data", json.dumps(data)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": result.stdout or result.stderr}


def get_wiki_nodes(space_id, parent_token="", depth=0):
    """递归获取wiki节点（包括子节点）。"""
    if depth > 3:
        return []
    
    path = f"/open-apis/wiki/v2/spaces/{space_id}/nodes"
    if parent_token:
        path += f"?parent_node_token={parent_token}"
    
    resp = lark_api("GET", path)
    items = resp.get("data", {}).get("items", [])
    results = []
    
    for node in items:
        node_token = node.get("node_token")
        node_type = node.get("node_type")
        title = node.get("title")
        
        results.append({
            "title": title,
            "node_token": node_token,
            "node_type": node_type,
            "depth": depth
        })
        
        # 递归子节点
        if node_type == "origin" and node_token:
            children = get_wiki_nodes(space_id, node_token, depth + 1)
            results.extend(children)
    
    return results


def get_wiki_doc_token(space_id, node_token):
    """获取wiki节点指向的文档token和类型。
    Wiki节点结构：obj_token=文档token, obj_type=文档类型, owner=当前所有者
    """
    resp = lark_api("GET", f"/open-apis/wiki/v2/spaces/{space_id}/nodes/{node_token}")
    node = resp.get("data", {}).get("node", {})
    return node.get("obj_token"), node.get("obj_type"), node.get("owner")


def transfer_owner(file_type, token, target_id, member_type="openid"):
    data = {
        "type": file_type,
        "token": token,
        "owner": {
            "member_type": member_type,
            "member_id": target_id,
        },
        "remove_old_owner": False,
        "cancel_notify": False,
    }
    return lark_api("POST", "/open-apis/drive/permission/member/transfer", data)


def main():
    parser = argparse.ArgumentParser(description="飞书Wiki文档所有权转移")
    parser.add_argument("--target", required=True, help="目标用户ID (open_id)")
    parser.add_argument("--space", required=True, help="Wiki space_id")
    parser.add_argument("--member-type", default="openid")
    parser.add_argument("--list", action="store_true", help="dry-run，只列出")
    parser.add_argument("--depth", type=int, default=3, help="最大递归深度")
    args = parser.parse_args()

    print(f"扫描 Wiki space: {args.space} ...")
    
    # 获取wiki节点树
    visited_tokens = set()
    nodes_to_check = [(args.space, "", 0)]
    all_nodes = []
    
    while nodes_to_check:
        space_id, parent, depth = nodes_to_check.pop(0)
        if depth > args.depth:
            continue
        
        path = f"/open-apis/wiki/v2/spaces/{space_id}/nodes"
        if parent:
            path += f"?parent_node_token={parent}"
        
        resp = lark_api("GET", path)
        items = resp.get("data", {}).get("items", [])
        
        for node in items:
            nt = node.get("node_token")
            if nt in visited_tokens:
                continue
            visited_tokens.add(nt)
            
            all_nodes.append({
                "title": node.get("title"),
                "node_token": nt,
                "node_type": node.get("node_type"),
                "depth": depth
            })
            
            if node.get("node_type") == "origin" and nt:
                nodes_to_check.append((space_id, nt, depth + 1))

    print(f"共扫描 {len(all_nodes)} 个节点")

    # 过滤有文档的节点并转移
    transferred = skipped = failed = 0
    
    for node in all_nodes:
        if node["node_type"] != "origin":
            continue
        
        indent = "  " * (node["depth"] + 1)
        print(f"{indent}📄 {node['title']}")
        
        docs_token, docs_type, current_owner = get_wiki_doc_token(args.space, node["node_token"])
        if not docs_token:
            print(f"{indent}  (无关联文档或无权限)")
            continue
        
        ftype = docs_type or "docx"
        print(f"{indent}  token={docs_token} type={ftype} owner={current_owner}")
        
        # 跳过已是目标所有者的
        if current_owner == args.target:
            print(f"{indent}  ✅ 已是目标所有者，跳过")
            skipped += 1
            print()
            continue
        
        if args.list:
            print(f"{indent}  [DRY-RUN] 将转移 -> {args.target}")
            transferred += 1
        else:
            resp = transfer_owner(ftype, docs_token, args.target, args.member_type)
            if resp.get("code") == 0:
                print(f"{indent}  ✅ 转移成功")
                transferred += 1
            else:
                print(f"{indent}  ❌ 失败: {resp.get('msg', resp)}")
                failed += 1
        print()
    
    print(f"\n=== 汇总 ===")
    print(f"  转移: {transferred}")
    print(f"  失败: {failed}")
    print(f"  跳过(含无关联文档): {skipped}")


if __name__ == "__main__":
    main()
