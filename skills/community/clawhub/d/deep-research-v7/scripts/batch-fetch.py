#!/usr/bin/env python3
"""
batch-fetch.py - 批量网页抓取，生成深度研究卡片

支持:
- 从URL列表文件批量抓取
- 并发控制(默认3个并发)
- 随机延迟(反爬)
- 进度显示
- 失败重试
- 断点续抓

用法:
  python batch-fetch.py urls.txt --domain healthcare --output sources/
  python batch-fetch.py urls.txt --prefix card-mckinsey --concurrent 5 -v

URL文件格式 (每行一个):
  https://www.mckinsey.com/article1
  https://www.mckinsey.com/article2
  # 这是注释
  https://arxiv.org/abs/2301.12345
"""

import sys
import json
import time
import random
import argparse
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Dict, Any, Optional


DEFAULT_CONCURRENT = 3
DEFAULT_DELAY = (1, 3)  # 随机延迟范围(秒)
CHECKPOINT_FILE = ".batch_fetch_checkpoint.json"


def parse_url_file(url_file: Path) -> List[str]:
    """解析URL列表文件"""
    urls = []
    
    with open(url_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            urls.append(line)
    
    return urls


def load_checkpoint(output_dir: Path) -> Dict[str, Any]:
    """加载断点记录"""
    checkpoint_path = output_dir / CHECKPOINT_FILE
    
    if checkpoint_path.exists():
        with open(checkpoint_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {"completed": [], "failed": [], "total": 0}


def save_checkpoint(output_dir: Path, checkpoint: Dict[str, Any]):
    """保存断点记录"""
    checkpoint_path = output_dir / CHECKPOINT_FILE
    
    with open(checkpoint_path, 'w', encoding='utf-8') as f:
        json.dump(checkpoint, f, indent=2, ensure_ascii=False)


def fetch_single_url(
    url: str,
    card_id: str,
    domain: str,
    timeout: int,
    retries: int,
    output_dir: Path,
    verbose: bool
) -> Dict[str, Any]:
    """
    抓取单个URL
    
    Returns:
        结果字典，包含success、card_id、error等
    """
    
    # 构造fetch-card-from-web命令
    script_path = Path(__file__).parent / "fetch-card-from-web.py"
    
    cmd = [
        "python3", str(script_path),
        card_id,
        url,
        "--domain", domain,
        "--timeout", str(timeout),
        "--retries", str(retries)
    ]
    
    result = {
        "url": url,
        "card_id": card_id,
        "success": False,
        "error": None,
        "output_file": None
    }
    
    try:
        if verbose:
            print(f"[Batch] 开始抓取: {url[:60]}...")
        
        start_time = time.time()
        
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout * retries + 60
        )
        
        elapsed = time.time() - start_time
        
        if proc.returncode == 0:
            # 检查输出文件
            json_file = output_dir / f"{card_id}.json"
            if json_file.exists():
                result["success"] = True
                result["output_file"] = str(json_file)
                result["elapsed"] = elapsed
            else:
                result["error"] = "JSON文件未生成"
        else:
            result["error"] = f"抓取失败: {proc.stderr[:200]}"
        
    except subprocess.TimeoutExpired:
        result["error"] = "超时"
    except Exception as e:
        result["error"] = str(e)
    
    return result


def batch_fetch(
    url_file: Path,
    domain: str,
    output_dir: Path,
    prefix: str = "card-batch",
    concurrent: int = DEFAULT_CONCURRENT,
    delay_range: tuple = DEFAULT_DELAY,
    timeout: int = 60,
    retries: int = 3,
    resume: bool = True,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    批量抓取主函数
    
    Returns:
        统计信息字典
    """
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 解析URL列表
    urls = parse_url_file(url_file)
    
    if not urls:
        print("❌ URL列表为空")
        return {"total": 0, "success": 0, "failed": 0}
    
    print(f"📋 URL列表: {len(urls)} 个")
    
    # 加载断点
    checkpoint = load_checkpoint(output_dir)
    
    # 过滤已完成的
    if resume:
        completed_urls = set(checkpoint.get("completed", []))
        failed_urls = set(checkpoint.get("failed", []))
        
        # 重试失败的
        urls_to_fetch = [u for u in urls if u not in completed_urls]
        
        print(f"   已完成: {len(completed_urls)}")
        print(f"   待抓取: {len(urls_to_fetch)}")
        print(f"   将重试: {len(failed_urls)} 个失败项")
    else:
        urls_to_fetch = urls
        checkpoint = {"completed": [], "failed": [], "total": len(urls)}
    
    if not urls_to_fetch:
        print("✅ 所有URL已处理完毕")
        return {
            "total": len(urls),
            "success": len(checkpoint.get("completed", [])),
            "failed": len(checkpoint.get("failed", []))
        }
    
    # 生成卡片ID列表
    start_index = len(checkpoint.get("completed", [])) + 1
    card_ids = [f"{prefix}-{i:03d}" for i in range(start_index, start_index + len(urls_to_fetch))]
    
    # 结果统计
    success_count = len(checkpoint.get("completed", []))
    failed_count = len(checkpoint.get("failed", []))
    
    print(f"\n🚀 开始批量抓取 (并发: {concurrent}, 延迟: {delay_range[0]}-{delay_range[1]}s)")
    print("-" * 60)
    
    # 并发抓取
    with ThreadPoolExecutor(max_workers=concurrent) as executor:
        futures = {}
        
        for i, (url, card_id) in enumerate(zip(urls_to_fetch, card_ids)):
            # 随机延迟（第一个不延迟）
            if i > 0:
                delay = random.uniform(*delay_range)
                if verbose:
                    print(f"[Batch] 延迟 {delay:.1f}s...")
                time.sleep(delay)
            
            future = executor.submit(
                fetch_single_url,
                url, card_id, domain, timeout, retries,
                output_dir, verbose
            )
            futures[future] = (url, card_id)
        
        # 收集结果
        for future in as_completed(futures):
            url, card_id = futures[future]
            
            try:
                result = future.result()
                
                if result["success"]:
                    success_count += 1
                    checkpoint["completed"].append(url)
                    print(f"✅ [{card_id}] {url[:50]}... ({result.get('elapsed', 0):.1f}s)")
                else:
                    failed_count += 1
                    if url not in checkpoint["failed"]:
                        checkpoint["failed"].append(url)
                    print(f"❌ [{card_id}] {url[:50]}... - {result['error']}")
                
                # 保存断点
                save_checkpoint(output_dir, checkpoint)
                
            except Exception as e:
                failed_count += 1
                print(f"❌ [{card_id}] 异常: {e}")
    
    # 最终统计
    print("-" * 60)
    print(f"\n📊 批量抓取完成!")
    print(f"   总计: {len(urls)}")
    print(f"   成功: {success_count} ({success_count/len(urls)*100:.1f}%)")
    print(f"   失败: {failed_count}")
    
    if checkpoint.get("failed"):
        print(f"\n⚠️  失败列表:")
        for url in checkpoint["failed"]:
            print(f"   - {url}")
    
    return {
        "total": len(urls),
        "success": success_count,
        "failed": failed_count,
        "output_dir": str(output_dir)
    }


def main():
    parser = argparse.ArgumentParser(
        description="批量网页抓取，生成深度研究卡片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础用法
  python batch-fetch.py urls.txt --domain healthcare
  
  # 指定前缀和输出目录
  python batch-fetch.py urls.txt --prefix mckinsey --output sources/mckinsey/
  
  # 增加并发和超时（海外网站）
  python batch-fetch.py urls.txt --domain insurance --concurrent 5 --timeout 90
  
  # 从头开始（不使用断点续抓）
  python batch-fetch.py urls.txt --no-resume
  
URL文件格式:
  # 每行一个URL，#开头为注释
  https://www.mckinsey.com/industries/healthcare/article1
  https://www.mckinsey.com/industries/healthcare/article2
  https://arxiv.org/abs/2301.12345
        """
    )
    
    parser.add_argument("url_file", type=Path, help="URL列表文件路径")
    parser.add_argument("--domain", "-d", default="general",
                       help="研究领域 (default: general)")
    parser.add_argument("--output", "-o", type=Path, default=Path("sources"),
                       help="输出目录 (default: sources/)")
    parser.add_argument("--prefix", "-p", default="card-batch",
                       help="卡片ID前缀 (default: card-batch)")
    parser.add_argument("--concurrent", "-c", type=int, default=DEFAULT_CONCURRENT,
                       help=f"并发数 (default: {DEFAULT_CONCURRENT})")
    parser.add_argument("--delay-min", type=float, default=DEFAULT_DELAY[0],
                       help=f"最小延迟秒数 (default: {DEFAULT_DELAY[0]})")
    parser.add_argument("--delay-max", type=float, default=DEFAULT_DELAY[1],
                       help=f"最大延迟秒数 (default: {DEFAULT_DELAY[1]})")
    parser.add_argument("--timeout", "-t", type=int, default=60,
                       help="单个URL超时时间（秒）(default: 60)")
    parser.add_argument("--retries", "-r", type=int, default=3,
                       help="失败重试次数 (default: 3)")
    parser.add_argument("--no-resume", action="store_true",
                       help="禁用断点续抓，从头开始")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="详细日志")
    
    args = parser.parse_args()
    
    if not args.url_file.exists():
        print(f"❌ URL文件不存在: {args.url_file}")
        sys.exit(1)
    
    stats = batch_fetch(
        url_file=args.url_file,
        domain=args.domain,
        output_dir=args.output,
        prefix=args.prefix,
        concurrent=args.concurrent,
        delay_range=(args.delay_min, args.delay_max),
        timeout=args.timeout,
        retries=args.retries,
        resume=not args.no_resume,
        verbose=args.verbose
    )
    
    # 返回码：全部成功为0，有失败为1
    if stats["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
