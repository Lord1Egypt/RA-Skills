#!/usr/bin/env python3
"""
深度学习课程PPT - 完整示例
演示如何使用图文并茂PPT生成技能
"""

import os
import sys

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from illustrated_ppt import IllustratedPPTGenerator

def deep_learning_course():
    """深度学习课程PPT示例"""
    topic = "深度学习基础课程"
    scene = "education"
    
    slides = [
        {
            "type": "cover",
            "title": "深度学习基础课程",
            "content": "人工智能 · 理论课"
        },
        {
            "type": "toc",
            "title": "目 录",
            "chapters": [
                "神经网络基础",
                "卷积神经网络 CNN",
                "循环神经网络 RNN",
                "Transformer 与注意力机制"
            ]
        },
        {
            "type": "content",
            "title": "神经网络基础",
            "bullets": [
                "神经元模型：输入、权重、激活函数",
                "常用激活函数：Sigmoid、ReLU、Tanh",
                "损失函数：均方误差、交叉熵",
                "反向传播算法原理"
            ]
        },
        {
            "type": "content",
            "title": "卷积神经网络 CNN",
            "bullets": [
                "卷积层：滤波器与特征提取",
                "池化层：最大池化与平均池化",
                "经典架构：LeNet、AlexNet、VGG",
                "应用场景：图像分类、目标检测"
            ]
        },
        {
            "type": "content",
            "title": "循环神经网络 RNN",
            "bullets": [
                "序列数据处理：时间步与隐藏状态",
                "长短期记忆网络 LSTM",
                "门控循环单元 GRU",
                "应用：文本生成、机器翻译"
            ]
        },
        {
            "type": "code",
            "title": "PyTorch 简单网络示例",
            "content": """import torch
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(784, 256)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(256, 10)

    def forward(self, x):
        x = x.view(-1, 784)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = SimpleNet()
print(model)"""
        },
        {
            "type": "content",
            "title": "Transformer 与注意力机制",
            "bullets": [
                "自注意力机制（Self-Attention）",
                "多头注意力（Multi-Head Attention）",
                "位置编码与序列建模",
                "BERT / GPT 等预训练模型"
            ]
        },
        {
            "type": "summary",
            "title": "课程总结",
            "bullets": [
                "掌握神经网络核心概念与原理",
                "理解 CNN、RNN、Transformer 架构",
                "能够使用 PyTorch 构建简单网络",
                "完成课后练习巩固所学知识"
            ]
        },
        {
            "type": "homework",
            "title": "课后作业",
            "bullets": [
                "复习神经元模型与激活函数",
                "使用 PyTorch 实现一个简单 CNN",
                "对比 LSTM 与 GRU 的差异",
                "阅读 Transformer 论文（选读）"
            ]
        },
        {
            "type": "closing",
            "title": "本文由AI辅助创作",
            "content": "作者：TJMtaotao | 发表于：MEITUSTYLE"
        }
    ]
    
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    if not api_key:
        print("❌ 请设置环境变量 MINIMAX_API_KEY")
        return
    
    generator = IllustratedPPTGenerator(api_key)
    result = generator.generate(topic, slides, scene, "/tmp")
    print(f"\n🎉 深度学习课程PPT已生成: {result['output_path']}")


def business_presentation():
    """商业演示PPT示例"""
    topic = "产品发布会演示"
    scene = "business"
    
    slides = [
        {"type": "cover", "title": "产品发布会", "content": "2026年新品发布"},
        {"type": "toc", "title": "目录", "chapters": ["产品介绍", "核心优势", "市场分析", "合作方案"]},
        {"type": "content", "title": "产品介绍", "bullets": ["产品背景", "主要功能", "技术架构", "应用场景"]},
        {"type": "content", "title": "核心优势", "bullets": ["高性能", "易用性", "安全性", "扩展性"]},
        {"type": "content", "title": "市场分析", "bullets": ["市场规模", "竞争分析", "目标用户", "增长趋势"]},
        {"type": "summary", "title": "核心要点", "bullets": ["领先技术", "市场认可", "商业价值"]},
        {"type": "closing", "title": "感谢观看", "content": "联系方式：contact@example.com"},
    ]
    
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    generator = IllustratedPPTGenerator(api_key)
    result = generator.generate(topic, slides, scene, "/tmp")
    print(f"\n🎉 商业演示PPT已生成: {result['output_path']}")


def tech分享():
    """技术分享PPT示例"""
    topic = "云原生技术架构分享"
    scene = "tech"
    
    slides = [
        {"type": "cover", "title": "云原生技术架构", "content": "Docker + Kubernetes"},
        {"type": "toc", "title": "内容大纲", "chapters": ["容器基础", "Kubernetes核心", "服务网格", "实践案例"]},
        {"type": "content", "title": "容器基础", "bullets": ["Docker核心概念", "镜像构建", "容器编排", "网络配置"]},
        {"type": "content", "title": "Kubernetes核心", "bullets": ["Pod/Deployment", "Service/Ingress", "ConfigMap/Secret", "集群管理"]},
        {"type": "code", "title": "Kubernetes YAML示例", "content": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    spec:
      containers:
      - name: web
        image: myapp:v1
        ports:
        - containerPort: 8080"""},
        {"type": "summary", "title": "实践要点", "bullets": ["Infrastructure as Code", "GitOps工作流", "自动化运维"]},
        {"type": "closing", "title": "Q & A", "content": "谢谢大家"},
    ]
    
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    generator = IllustratedPPTGenerator(api_key)
    result = generator.generate(topic, slides, scene, "/tmp")
    print(f"\n🎉 技术分享PPT已生成: {result['output_path']}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="图文并茂PPT生成示例")
    parser.add_argument("type", choices=["dl", "business", "tech", "all"],
                       help="示例类型: dl=深度学习, business=商业演示, tech=技术分享, all=全部")
    
    args = parser.parse_args()
    
    if args.type == "dl":
        deep_learning_course()
    elif args.type == "business":
        business_presentation()
    elif args.type == "tech":
        tech分享()
    elif args.type == "all":
        print("=" * 50)
        print("执行所有示例...")
        print("=" * 50)
        deep_learning_course()
        print()
        business_presentation()
        print()
        tech分享()
        print()
        print("=" * 50)
        print("✅ 全部示例执行完成！")
        print("=" * 50)