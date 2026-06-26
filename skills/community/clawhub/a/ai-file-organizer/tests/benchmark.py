#!/usr/bin/env python3
"""
AI File Organizer - 性能基准测试

测试不同配置下的性能表现
"""

import os
import sys
import time
import tempfile
import shutil
import statistics
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from organizer import AIFileOrganizer, FileStats


def create_test_files(directory: str, count: int, sizes: dict = None):
    """创建测试文件"""
    os.makedirs(directory, exist_ok=True)
    
    if sizes is None:
        sizes = {
            'small': (1024, 0.6),      # 1KB, 60%
            'medium': (102400, 0.3),   # 100KB, 30%
            'large': (1048576, 0.1),   # 1MB, 10%
        }
    
    extensions = ['.pdf', '.docx', '.jpg', '.png', '.mp4', '.py', '.js', '.zip']
    
    print(f"📝 创建 {count} 个测试文件...")
    
    for i in range(count):
        # 确定文件大小
        rand = i / count
        cumulative = 0
        size_range = sizes['small']
        
        for size_name, (size, ratio) in sizes.items():
            cumulative += ratio
            if rand < cumulative:
                size_range = (size, ratio)
                break
        
        size = size_range[0]
        
        # 生成文件内容
        ext = extensions[i % len(extensions)]
        filename = f"test_file_{i:06d}{ext}"
        filepath = os.path.join(directory, filename)
        
        with open(filepath, 'wb') as f:
            # 写入随机数据
            chunk_size = 8192
            remaining = size
            while remaining > 0:
                write_size = min(chunk_size, remaining)
                f.write(os.urandom(write_size))
                remaining -= write_size
        
        if (i + 1) % 1000 == 0:
            print(f"  已创建 {i + 1}/{count} 个文件")
    
    print(f"✅ 测试文件创建完成")


def run_benchmark(test_dir: str, target_dir: str, concurrent: int = 10, 
                  cache_enabled: bool = True, label: str = ""):
    """运行基准测试"""
    
    # 创建整理师
    config = {
        'logging': {'level': 'WARNING'},
        'cache': {'enabled': cache_enabled}
    }
    
    organizer = AIFileOrganizer(config, cache_enabled=cache_enabled)
    
    # 运行测试
    print(f"\n{'='*60}")
    print(f"🚀 基准测试：{label or f'并发={concurrent}, 缓存={cache_enabled}'}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    report = organizer.organize_files(
        source_dir=test_dir,
        target_dir=target_dir,
        max_concurrent=concurrent
    )
    
    elapsed = time.time() - start_time
    
    # 输出结果
    print(f"\n📊 测试结果:")
    print(f"  总文件数：{report.stats['total_files']}")
    print(f"  成功处理：{report.stats['processed']}")
    print(f"  失败：{report.stats['errors']}")
    print(f"  耗时：{elapsed:.2f}秒")
    print(f"  速度：{report.stats['processed']/elapsed:.1f} 个/秒")
    
    if cache_enabled:
        total_cache = report.stats['cache_hits'] + report.stats['cache_misses']
        hit_rate = (report.stats['cache_hits'] / total_cache * 100) if total_cache > 0 else 0
        print(f"  缓存命中：{report.stats['cache_hits']} ({hit_rate:.1f}%)")
    
    return {
        'label': label or f'concurrent={concurrent}',
        'total_files': report.stats['total_files'],
        'processed': report.stats['processed'],
        'errors': report.stats['errors'],
        'elapsed': elapsed,
        'speed': report.stats['processed']/elapsed if elapsed > 0 else 0,
        'cache_hits': report.stats.get('cache_hits', 0),
        'cache_misses': report.stats.get('cache_misses', 0)
    }


def benchmark_concurrent_levels(test_dir: str, file_count: int = 1000):
    """测试不同并发级别的性能"""
    
    results = []
    concurrent_levels = [1, 5, 10, 20, 50]
    
    print("\n" + "="*60)
    print("📈 并发级别性能测试")
    print("="*60)
    
    for concurrent in concurrent_levels:
        # 创建临时目录
        test_subdir = os.path.join(test_dir, f'concurrent_{concurrent}')
        target_subdir = tempfile.mkdtemp()
        
        try:
            # 创建测试文件
            create_test_files(test_subdir, file_count // len(concurrent_levels))
            
            # 运行测试
            result = run_benchmark(
                test_subdir, 
                target_subdir, 
                concurrent=concurrent,
                cache_enabled=False,
                label=f"并发={concurrent}"
            )
            results.append(result)
            
        finally:
            # 清理
            if os.path.exists(test_subdir):
                shutil.rmtree(test_subdir)
            if os.path.exists(target_subdir):
                shutil.rmtree(target_subdir)
    
    # 输出对比
    print("\n" + "="*60)
    print("📊 并发级别对比")
    print("="*60)
    print(f"{'并发数':<10} {'速度 (个/秒)':<15} {'耗时 (秒)':<10} {'提升'}")
    print("-"*60)
    
    baseline = results[0]['speed']
    for result in results:
        improvement = (result['speed'] / baseline - 1) * 100 if baseline > 0 else 0
        print(f"{result['label']:<10} {result['speed']:<15.1f} {result['elapsed']:<10.2f} {improvement:+.1f}%")
    
    return results


def benchmark_cache_performance(test_dir: str, file_count: int = 500):
    """测试缓存性能"""
    
    print("\n" + "="*60)
    print("📈 缓存性能测试")
    print("="*60)
    
    results = []
    
    # 第一次运行（无缓存）
    test_subdir = os.path.join(test_dir, 'cache_test')
    target_subdir = tempfile.mkdtemp()
    
    try:
        create_test_files(test_subdir, file_count)
        
        print("\n📝 第一次运行（缓存未命中）...")
        result1 = run_benchmark(
            test_subdir, 
            target_subdir, 
            concurrent=10,
            cache_enabled=True,
            label="首次运行"
        )
        results.append(result1)
        
        # 第二次运行（有缓存）
        print("\n📝 第二次运行（缓存命中）...")
        target_subdir2 = tempfile.mkdtemp()
        result2 = run_benchmark(
            test_subdir, 
            target_subdir2, 
            concurrent=10,
            cache_enabled=True,
            label="缓存命中"
        )
        results.append(result2)
        
        # 输出对比
        print("\n" + "="*60)
        print("📊 缓存对比")
        print("="*60)
        
        improvement = (result1['elapsed'] / result2['elapsed'] - 1) * 100 if result2['elapsed'] > 0 else 0
        print(f"首次运行：{result1['elapsed']:.2f}秒 ({result1['speed']:.1f} 个/秒)")
        print(f"缓存命中：{result2['elapsed']:.2f}秒 ({result2['speed']:.1f} 个/秒)")
        print(f"性能提升：{improvement:+.1f}%")
        
    finally:
        if os.path.exists(test_subdir):
            shutil.rmtree(test_subdir)
        if os.path.exists(target_subdir):
            shutil.rmtree(target_subdir)
        if 'target_subdir2' in locals() and os.path.exists(target_subdir2):
            shutil.rmtree(target_subdir2)
    
    return results


def benchmark_file_sizes(test_dir: str):
    """测试不同文件大小的性能"""
    
    print("\n" + "="*60)
    print("📈 文件大小性能测试")
    print("="*60)
    
    size_configs = [
        {'small': (1024, 1.0)},           # 全部 1KB
        {'medium': (102400, 1.0)},        # 全部 100KB
        {'large': (1048576, 1.0)},        # 全部 1MB
        {'mixed': (1024, 0.6, 102400, 0.3, 1048576, 0.1)},  # 混合
    ]
    
    results = []
    
    for size_config in size_configs:
        config_name = list(size_config.keys())[0]
        test_subdir = os.path.join(test_dir, f'size_{config_name}')
        target_subdir = tempfile.mkdtemp()
        
        try:
            # 创建特定大小的测试文件
            if config_name == 'mixed':
                sizes = {'small': (1024, 0.6), 'medium': (102400, 0.3), 'large': (1048576, 0.1)}
            else:
                sizes = {config_name: (size_config[config_name][0], 1.0)}
            
            create_test_files(test_subdir, 200, sizes)
            
            result = run_benchmark(
                test_subdir,
                target_subdir,
                concurrent=10,
                cache_enabled=False,
                label=f"文件大小={config_name}"
            )
            results.append(result)
            
        finally:
            if os.path.exists(test_subdir):
                shutil.rmtree(test_subdir)
            if os.path.exists(target_subdir):
                shutil.rmtree(target_subdir)
    
    # 输出对比
    print("\n" + "="*60)
    print("📊 文件大小对比")
    print("="*60)
    print(f"{'文件大小':<15} {'速度 (个/秒)':<15} {'耗时 (秒)':<10}")
    print("-"*60)
    
    for result in results:
        print(f"{result['label']:<15} {result['speed']:<15.1f} {result['elapsed']:<10.2f}")
    
    return results


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI File Organizer 性能基准测试')
    parser.add_argument('--test-dir', type=str, default=None, help='测试目录')
    parser.add_argument('--files', type=int, default=1000, help='测试文件数量')
    parser.add_argument('--test', type=str, choices=['concurrent', 'cache', 'sizes', 'all'],
                       default='all', help='测试类型')
    
    args = parser.parse_args()
    
    # 创建测试目录
    test_dir = args.test_dir or tempfile.mkdtemp(prefix='ai_organizer_benchmark_')
    print(f"📁 测试目录：{test_dir}")
    
    try:
        if args.test in ['concurrent', 'all']:
            benchmark_concurrent_levels(test_dir, args.files)
        
        if args.test in ['cache', 'all']:
            benchmark_cache_performance(test_dir, min(args.files, 500))
        
        if args.test in ['sizes', 'all']:
            benchmark_file_sizes(test_dir)
        
        print("\n" + "="*60)
        print("✅ 所有基准测试完成")
        print("="*60)
    
    finally:
        # 清理测试目录（如果是指定的则不清理）
        if not args.test_dir and os.path.exists(test_dir):
            print(f"\n🧹 清理测试目录：{test_dir}")
            shutil.rmtree(test_dir)


if __name__ == '__main__':
    main()
