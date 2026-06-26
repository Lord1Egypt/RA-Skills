#!/usr/bin/env python3
"""
🎪 JSON Performance Engine - AetherCore v3.3.4
Night Market Intelligence Technical Serviceization Practice
High-performance JSON optimization system
"""

import json
import time
import gzip
import zlib
import hashlib
from typing import Dict, List, Any, Union
from dataclasses import dataclass, asdict
from functools import lru_cache
import orjson  # High-performance JSON library
import ujson   # UltraJSON library
import rapidjson  # RapidJSON library

@dataclass
class PerformanceMetrics:
    """Performance metrics for JSON operations"""
    parse_time_ms: float
    serialize_time_ms: float
    memory_usage_bytes: int
    compression_ratio: float
    operations_per_second: float

class JSONPerformanceEngine:
    """High-performance JSON optimization engine"""
    
    def __init__(self, use_orjson: bool = True, use_compression: bool = False):
        """
        Initialize JSON performance engine
        
        Args:
            use_orjson: Use orjson for maximum performance
            use_compression: Enable compression for large data
        """
        self.use_orjson = use_orjson
        self.use_compression = use_compression
        self.cache = {}
        
    def optimize(self, data: Union[Dict, List, str], path: str = None) -> Dict:
        """
        Optimize JSON data for performance
        
        Args:
            data: JSON data to optimize
            path: Optional file path for file-based optimization
            
        Returns:
            Dict with optimization results
        """
        print(f"🔧 Optimizing JSON data...")
        
        if isinstance(data, str):
            # If data is a string, try to parse it
            try:
                data = self.parse(data)
            except Exception as e:
                return {"status": "error", "message": f"Failed to parse data: {e}"}
        
        # Measure original performance
        original_metrics = self.measure_performance(data)
        
        # Apply optimizations
        optimized_data = self.apply_optimizations(data)
        
        # Measure optimized performance
        optimized_metrics = self.measure_performance(optimized_data)
        
        # Calculate improvements
        improvement = {
            "parse_time_improvement": original_metrics.parse_time_ms / optimized_metrics.parse_time_ms,
            "serialize_time_improvement": original_metrics.serialize_time_ms / optimized_metrics.serialize_time_ms,
            "memory_reduction": 1 - (optimized_metrics.memory_usage_bytes / original_metrics.memory_usage_bytes),
            "compression_gain": optimized_metrics.compression_ratio,
            "ops_per_second_gain": optimized_metrics.operations_per_second / original_metrics.operations_per_second
        }
        
        result = {
            "status": "success",
            "original_metrics": asdict(original_metrics),
            "optimized_metrics": asdict(optimized_metrics),
            "improvement": improvement,
            "optimized_files": 1 if path else 0,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # If path provided, write optimized data
        if path:
            try:
                self.write_optimized_data(optimized_data, path)
                result["file_written"] = path
                result["optimized_files"] = 1
            except Exception as e:
                result["file_error"] = str(e)
        
        return result
    
    def parse(self, json_str: str) -> Any:
        """Parse JSON string with optimal performance"""
        if self.use_orjson:
            try:
                return orjson.loads(json_str.encode('utf-8'))
            except Exception:
                # Fallback to standard JSON
                return json.loads(json_str)
        else:
            return json.loads(json_str)
    
    def serialize(self, data: Any) -> str:
        """Serialize data to JSON string with optimal performance"""
        if self.use_orjson:
            try:
                return orjson.dumps(data).decode('utf-8')
            except Exception:
                # Fallback to standard JSON
                return json.dumps(data)
        else:
            return json.dumps(data)
    
    def measure_performance(self, data: Any) -> PerformanceMetrics:
        """Measure performance metrics for JSON operations"""
        # Measure parse time
        json_str = self.serialize(data)
        
        parse_start = time.perf_counter()
        for _ in range(100):
            self.parse(json_str)
        parse_time_ms = (time.perf_counter() - parse_start) * 10  # Average per operation
        
        # Measure serialize time
        serialize_start = time.perf_counter()
        for _ in range(100):
            self.serialize(data)
        serialize_time_ms = (time.perf_counter() - serialize_start) * 10  # Average per operation
        
        # Calculate memory usage
        memory_usage = len(json_str.encode('utf-8'))
        
        # Calculate compression ratio
        if self.use_compression:
            compressed = gzip.compress(json_str.encode('utf-8'))
            compression_ratio = len(compressed) / memory_usage
        else:
            compression_ratio = 1.0
        
        # Calculate operations per second
        total_time_ms = parse_time_ms + serialize_time_ms
        operations_per_second = 1000 / total_time_ms if total_time_ms > 0 else 0
        
        return PerformanceMetrics(
            parse_time_ms=parse_time_ms,
            serialize_time_ms=serialize_time_ms,
            memory_usage_bytes=memory_usage,
            compression_ratio=compression_ratio,
            operations_per_second=operations_per_second
        )
    
    def apply_optimizations(self, data: Any) -> Any:
        """Apply performance optimizations to data"""
        # Remove null values
        if isinstance(data, dict):
            optimized = {}
            for key, value in data.items():
                if value is not None:
                    if isinstance(value, (dict, list)):
                        optimized[key] = self.apply_optimizations(value)
                    else:
                        optimized[key] = value
            return optimized
        
        # Optimize lists
        elif isinstance(data, list):
            optimized = []
            for item in data:
                if item is not None:
                    if isinstance(item, (dict, list)):
                        optimized.append(self.apply_optimizations(item))
                    else:
                        optimized.append(item)
            return optimized
        
        # Return other types as-is
        else:
            return data
    
    def write_optimized_data(self, data: Any, path: str):
        """Write optimized data to file"""
        optimized_json = self.serialize(data)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(optimized_json)
        
        print(f"✅ Optimized data written to: {path}")
    
    @lru_cache(maxsize=128)
    def cached_parse(self, json_str: str) -> Any:
        """Cached JSON parsing for repeated operations"""
        return self.parse(json_str)
    
    def benchmark_libraries(self, data: Any) -> Dict:
        """Benchmark different JSON libraries"""
        print("📊 Benchmarking JSON libraries...")
        
        results = {}
        json_str = json.dumps(data)
        
        # Test orjson
        try:
            start = time.perf_counter()
            for _ in range(100):
                orjson.loads(json_str.encode('utf-8'))
                orjson.dumps(data)
            results['orjson'] = (time.perf_counter() - start) * 10
        except Exception as e:
            results['orjson'] = {"error": str(e)}
        
        # Test ujson
        try:
            start = time.perf_counter()
            for _ in range(100):
                ujson.loads(json_str)
                ujson.dumps(data)
            results['ujson'] = (time.perf_counter() - start) * 10
        except Exception as e:
            results['ujson'] = {"error": str(e)}
        
        # Test rapidjson
        try:
            start = time.perf_counter()
            for _ in range(100):
                rapidjson.loads(json_str)
                rapidjson.dumps(data)
            results['rapidjson'] = (time.perf_counter() - start) * 10
        except Exception as e:
            results['rapidjson'] = {"error": str(e)}
        
        # Test standard json
        start = time.perf_counter()
        for _ in range(100):
            json.loads(json_str)
            json.dumps(data)
        results['stdlib'] = (time.perf_counter() - start) * 10
        
        return results

# Example usage
if __name__ == "__main__":
    # Create test data
    test_data = {
        "version": "v3.3.4",
        "description": "AetherCore Night Market Intelligence Performance Test",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data": {
            "items": [{"id": i, "name": f"Item {i}", "value": i * 10} for i in range(100)],
            "metadata": {"author": "AetherClaw", "license": "MIT"}
        }
    }
    
    # Create engine and optimize
    engine = JSONPerformanceEngine(use_orjson=True)
    result = engine.optimize(test_data)
    
    print("🎪 JSON Performance Engine Test Results:")
    print(f"  Parse Time: {result['optimized_metrics']['parse_time_ms']:.3f}ms")
    print(f"  Serialize Time: {result['optimized_metrics']['serialize_time_ms']:.3f}ms")
    print(f"  Operations/Second: {result['optimized_metrics']['operations_per_second']:.0f}")
    print(f"  Improvement: {result['improvement']['ops_per_second_gain']:.1f}x")
    
    # Benchmark libraries
    benchmark_results = engine.benchmark_libraries(test_data)
    print("\n📊 Library Benchmark Results:")
    for lib, time_ms in benchmark_results.items():
        if isinstance(time_ms, dict):
            print(f"  {lib}: {time_ms.get('error', 'Error')}")
        else:
            print(f"  {lib}: {time_ms:.3f}ms")