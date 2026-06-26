#!/usr/bin/env python3
"""
课程PPT生成脚本
根据课程主题和学科领域生成教学PPT
"""

import sys
import json
import os
from pathlib import Path

def generate_course_ppt(topic, subject="数据科学", course_type="理论课", pages=15):
    """生成课程PPT内容结构"""
    
    structure = {
        "title": topic,
        "subject": subject,
        "type": course_type,
        "pages": pages,
        "slides": []
    }
    
    # 封面
    structure["slides"].append({
        "type": "cover",
        "title": topic,
        "subtitle": f"{subject} - {course_type}",
        "author": "TJMtaotao",
        "institution": "广州华商学院",
        "date": "2026年"
    })
    
    # 目录
    structure["slides"].append({
        "type": "toc",
        "title": "目录",
        "chapters": ["课程介绍", "核心概念", "实践案例", "总结与作业"]
    })
    
    # 根据主题生成内容
    content_slides = generate_content_by_topic(topic, subject)
    structure["slides"].extend(content_slides)
    
    # 总结
    structure["slides"].append({
        "type": "summary",
        "title": "课程总结",
        "points": [
            "掌握核心概念和原理",
            "能够进行实践应用",
            "完成课后练习巩固"
        ]
    })
    
    # 作业
    structure["slides"].append({
        "type": "homework",
        "title": "课后作业",
        "exercises": [
            "复习本节核心知识点",
            "完成教材相关练习题",
            "实践操作并记录结果"
        ]
    })
    
    # AI标识
    structure["slides"].append({
        "type": "ai_mark",
        "content": "本文由AI辅助创作 / 作者：TJMtaotao / 发表于：MEITUSTYLE"
    })
    
    return structure


def generate_content_by_topic(topic, subject):
    """根据主题生成内容页"""
    slides = []
    
    topic_lower = topic.lower()
    subject_lower = subject.lower()
    
    # 数据预处理相关
    if "数据预处理" in topic or "预处理" in topic:
        slides = [
            {"type": "content", "title": "数据预处理概述", "points": ["数据清洗的重要性", "数据转换方法", "特征工程基础"]},
            {"type": "content", "title": "缺失值处理", "points": ["删除法", "填充法（均值/中位数/众数）", "插值法"]},
            {"type": "content", "title": "异常值检测", "points": ["3σ原则", "IQR方法", "孤立森林算法"]},
            {"type": "code", "title": "缺失值处理代码示例", "lang": "python"},
            {"type": "content", "title": "数据标准化", "points": ["Min-Max归一化", "Z-score标准化", "RobustScaler"]},
        ]
    # 深度学习相关
    elif "深度学习" in topic or "神经网络" in topic:
        slides = [
            {"type": "content", "title": "神经网络基础", "points": ["神经元模型", "激活函数", "损失函数"]},
            {"type": "content", "title": "卷积神经网络CNN", "points": ["卷积层原理", "池化层作用", "特征图理解"]},
            {"type": "content", "title": "循环神经网络RNN", "points": ["序列数据处理", "LSTM/GRU", "文本序列建模"]},
            {"type": "code", "title": "PyTorch简单网络示例", "lang": "python"},
            {"type": "content", "title": "Transformer与注意力机制", "points": ["自注意力机制", "多头注意力", "BERT/GPT架构"]},
        ]
    # Python编程相关
    elif "python" in topic_lower or "编程" in topic:
        slides = [
            {"type": "content", "title": "Python基础语法", "points": ["变量与数据类型", "控制流程语句", "函数定义与调用"]},
            {"type": "content", "title": "数据结构", "points": ["列表与元组", "字典与集合", "队列与栈"]},
            {"type": "code", "title": "基础语法示例", "lang": "python"},
            {"type": "content", "title": "面向对象编程", "points": ["类与对象", "继承与多态", "魔法方法"]},
            {"type": "content", "title": "文件与异常处理", "points": ["文件读写操作", "异常捕获机制", "上下文管理器"]},
        ]
    # 大数据技术相关
    elif "大数据" in topic:
        slides = [
            {"type": "content", "title": "大数据概述", "points": ["5V特征", "技术生态", "应用场景"]},
            {"type": "content", "title": "Hadoop生态", "points": ["HDFS分布式存储", "MapReduce计算", "YARN资源管理"]},
            {"type": "content", "title": "Spark核心", "points": ["RDD弹性分布式数据集", "DataFrameAPI", "SparkSQL查询"]},
            {"type": "code", "title": "Spark WordCount示例", "lang": "scala"},
            {"type": "content", "title": "Flink实时计算", "points": ["流处理架构", "时间窗口", "状态管理"]},
        ]
    # 机器学习相关
    elif "机器学习" in topic or "ML" in topic:
        slides = [
            {"type": "content", "title": "机器学习概述", "points": ["监督/无监督/强化学习", "训练集/验证集/测试集", "模型评估指标"]},
            {"type": "content", "title": "监督学习算法", "points": ["线性回归", "决策树", "支持向量机"]},
            {"type": "code", "title": "sklearn分类器示例", "lang": "python"},
            {"type": "content", "title": "无监督学习", "points": ["K-Means聚类", "层次聚类", "PCA降维"]},
            {"type": "content", "title": "模型优化", "points": ["正则化", "交叉验证", "超参数调优"]},
        ]
    # 默认内容
    else:
        slides = [
            {"type": "content", "title": "课程介绍", "points": ["学习目标", "课程内容概述", "先修知识要求"]},
            {"type": "content", "title": "核心概念", "points": ["基本概念定义", "原理讲解", "应用场景"]},
            {"type": "content", "title": "实践案例", "points": ["案例分析", "代码实现", "结果解读"]},
            {"type": "code", "title": "代码示例", "lang": "python"},
            {"type": "content", "title": "知识点总结", "points": ["重点回顾", "难点分析", "延伸学习"]},
        ]
    
    return slides


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_course_ppt.py <topic> [subject] [course_type] [pages]")
        print("Example: generate_course_ppt.py '深度学习' '人工智能' '理论课' 15")
        sys.exit(1)
    
    topic = sys.argv[1]
    subject = sys.argv[2] if len(sys.argv) > 2 else "数据科学"
    course_type = sys.argv[3] if len(sys.argv) > 3 else "理论课"
    pages = int(sys.argv[4]) if len(sys.argv) > 4 else 15
    
    result = generate_course_ppt(topic, subject, course_type, pages)
    
    # 输出JSON格式
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    
    # 保存到文件
    output_dir = Path.home() / "Desktop"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    safe_topic = topic.replace("/", "-").replace(" ", "_")
    output_file = output_dir / f"课程PPT_{safe_topic}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"\n✅ 内容结构已保存：{output_file}")


if __name__ == "__main__":
    main()