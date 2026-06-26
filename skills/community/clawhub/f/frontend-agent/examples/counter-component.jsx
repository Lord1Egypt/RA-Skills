import React, { useState } from 'react';
import { motion } from 'framer-motion';

/**
 * 智能计数器组件
 * 特性：
 * - Framer Motion 动画
 * - 本地存储持久化
 * - 可自定义步长
 * - 暗色模式支持
 */
export const SmartCounter = ({ 
  initialCount = 0, 
  step = 1,
  storageKey = 'counter-value'
}) => {
  // 从 localStorage 读取初始值
  const [count, setCount] = useState(() => {
    const saved = localStorage.getItem(storageKey);
    return saved ? parseInt(saved, 10) : initialCount;
  });

  // 持久化到 localStorage
  useEffect(() => {
    localStorage.setItem(storageKey, count.toString());
  }, [count, storageKey]);

  const increment = () => setCount(prev => prev + step);
  const decrement = () => setCount(prev => prev - step);
  const reset = () => setCount(initialCount);

  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className="inline-flex flex-col items-center gap-4 p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg"
    >
      <motion.div
        key={count}
        initial={{ scale: 1.2, color: '#3b82f6' }}
        animate={{ scale: 1, color: '#1f2937' }}
        className="text-5xl font-bold"
      >
        {count}
      </motion.div>

      <div className="flex gap-2">
        <button
          onClick={decrement}
          className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
        >
          -{step}
        </button>
        <button
          onClick={reset}
          className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
        >
          重置
        </button>
        <button
          onClick={increment}
          className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
        >
          +{step}
        </button>
      </div>
    </motion.div>
  );
};

// 使用示例
// <SmartCounter initialCount={10} step={5} storageKey="my-counter" />
