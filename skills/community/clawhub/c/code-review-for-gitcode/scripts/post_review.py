#!/usr/bin/env python3
"""
Step 5: Post code review comments to GitCode PR.
Reads formatted_review.json from Step 4.
"""

import sys
import json
import urllib.request
import urllib.error


def post_comment(owner: str, repo: str, pr_number: int, token: str, 
                 body: str, path: str = None, position: int = None):
    """Post a comment to GitCode PR."""
    url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{pr_number}/comments"
    
    # Build request data
    data = {
        "access_token": token,
        "body": body
    }
    
    if path:
        data["path"] = path
    if position:
        data["position"] = position
    
    # Encode data
    json_data = json.dumps(data).encode('utf-8')
    
    # Create request
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'OpenClaw-CodeReview/1.0'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"Comment posted successfully: {result.get('id', 'OK')}")
            return result
    except urllib.error.HTTPError as e:
        print(f"Error posting comment: {e.code} {e.reason}")
        print(e.read().decode('utf-8'))
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    if len(sys.argv) < 5:
        print("Usage: python post_review.py <owner> <repo> <pr_number> <token> [formatted_review.json]")
        print("")
        print("Parameters:")
        print("  owner: Repository owner (e.g., Ascend)")
        print("  repo: Repository name (e.g., msinsight)")
        print("  pr_number: PR number (e.g., 277)")
        print("  token: GitCode access token")
        print("  formatted_review.json: Path to formatted review JSON (default: formatted_review.json)")
        sys.exit(1)
    
    owner = sys.argv[1]
    repo = sys.argv[2]
    pr_number = int(sys.argv[3])
    token = sys.argv[4]
    review_file = sys.argv[5] if len(sys.argv) > 5 else "formatted_review.json"
    
    # Load formatted review from Step 4
    try:
        with open(review_file, 'r', encoding='utf-8') as f:
            review_data = json.load(f)
        comments = review_data.get('comments', [])
        meta = review_data.get('meta', {})
    except FileNotFoundError:
        print(f"Error: {review_file} not found.")
        print("Please run Step 4 (format_review.py) first.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {review_file}: {e}")
        sys.exit(1)
    
    if not comments:
        print("No comments to post.")
        sys.exit(0)
    
    # Show preview
    print("\n" + "="*60)
    print("代码检视意见预览")
    print("="*60)
    print(f"\n来源: {review_file}")
    print(f"总问题数: {meta.get('total_issues', 0)}")
    print(f"自动扫描: {meta.get('automated_count', 0)}")
    print(f"人工审查: {meta.get('manual_count', 0)}")
    print(f"将提交: {len(comments)} 条评论\n")
    
    for i, comment in enumerate(comments, 1):
        print(f"### 评论 #{i}")
        print(f"文件: {comment['path']} (行 {comment['position']})")
        print(f"严重程度: {comment['severity']}/10")
        print(f"类型: {comment['type']}")
        print(f"内容:\n{comment['body'][:500]}...")
        print()
    
    # Post individual comments only (no summary)
    print(f"\n正在提交 {len(comments)} 条评论...")
    for i, comment in enumerate(comments, 1):
        print(f"提交评论 #{i}...")
        post_comment(
            owner, repo, pr_number, token,
            comment["body"],
            comment.get("path"),
            comment.get("position")
        )
    
    print(f"\n✅ {len(comments)} 条评论已成功提交到 PR！")


if __name__ == '__main__':
    main()
