#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
期末试卷分析仪表盘 - 核心分析脚本
支持20+种可视化图表生成和公众号排版输出
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from scipy import stats
from sklearn.metrics import cohen_kappa_score
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class ExamAnalyzer:
    """试卷分析器 - 生成20+种可视化图表"""
    
    def __init__(self, data_path, class_name="未知班级"):
        """
        初始化分析器
        
        Args:
            data_path: 数据文件路径（Excel/CSV）
            class_name: 班级名称
        """
        self.data_path = data_path
        self.class_name = class_name
        self.df = None
        self.results = {}
        self.figures = []
        
        # 读取数据
        self.load_data()
        
        # 创建输出目录
        self.output_dir = f"exam_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(f"{self.output_dir}/charts", exist_ok=True)
        
    def load_data(self):
        """读取数据文件"""
        if self.data_path.endswith('.xlsx') or self.data_path.endswith('.xls'):
            self.df = pd.read_excel(self.data_path)
        elif self.data_path.endswith('.csv'):
            self.df = pd.read_csv(self.data_path)
        else:
            raise ValueError("不支持的文件格式，请使用Excel或CSV文件")
        
        # 假设最后一列是总分，其他列是各题得分
        self.student_col = self.df.columns[0]  # 第一列是学生标识
        self.score_cols = self.df.columns[1:]  # 其他列是题目得分
        
        print(f"✅ 数据加载成功：{len(self.df)}名学生，{len(self.score_cols)}道题目")
        
    def calculate_statistics(self):
        """计算基础统计数据"""
        # 计算总分（如果不存在）
        if '总分' not in self.df.columns:
            self.df['总分'] = self.df[self.score_cols].sum(axis=1)
        
        # 基础统计
        self.results['basic_stats'] = {
            '学生数': len(self.df),
            '平均分': self.df['总分'].mean(),
            '标准差': self.df['总分'].std(),
            '最高分': self.df['总分'].max(),
            '最低分': self.df['总分'].min(),
            '中位数': self.df['总分'].median(),
            '及格率': (self.df['总分'] >= 60).sum() / len(self.df) * 100,
            '优秀率': (self.df['总分'] >= 85).sum() / len(self.df) * 100,
        }
        
        # 各题统计
        self.results['question_stats'] = {}
        for col in self.score_cols:
            max_score = self.df[col].max()
            self.results['question_stats'][col] = {
                '平均分': self.df[col].mean(),
                '得分率': self.df[col].mean() / max_score * 100 if max_score > 0 else 0,
                '难度': 1 - self.df[col].mean() / max_score if max_score > 0 else 0,
                '区分度': self.calculate_discrimination(col),
            }
        
        print("✅ 基础统计计算完成")
        
    def calculate_discrimination(self, col):
        """计算题目区分度（高分组合低分组得分率之差）"""
        sorted_df = self.df.sort_values(by='总分', ascending=False)
        n = len(sorted_df)
        high_group = sorted_df.iloc[:n//3]  # 前1/3
        low_group = sorted_df.iloc[-n//3:]  # 后1/3
        
        high_avg = high_group[col].mean()
        low_avg = low_group[col].mean()
        max_score = self.df[col].max()
        
        if max_score > 0:
            return (high_avg - low_avg) / max_score
        return 0
    
    def calculate_reliability(self):
        """计算信度（Cronbach's α系数）"""
        # 简化版：使用题目间相关性估算
        scores = self.df[self.score_cols].values
        n_items = len(self.score_cols)
        
        if n_items < 2:
            self.results['reliability'] = 0
            return
        
        # 计算Cronbach's α
        item_variances = np.var(scores, axis=0)
        total_variance = np.var(np.sum(scores, axis=1))
        
        if total_variance > 0:
            alpha = (n_items / (n_items - 1)) * (1 - np.sum(item_variances) / total_variance)
            self.results['reliability'] = alpha
        else:
            self.results['reliability'] = 0
        
        print(f"✅ 信度分析完成：Cronbach's α = {self.results['reliability']:.3f}")
    
    # ==================== 可视化图表生成 ====================
    
    def plot_1_histogram(self):
        """1. 成绩分布直方图"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(self.df['总分'], bins=20, edgecolor='black', alpha=0.7, color='#3498db')
        ax.axvline(self.df['总分'].mean(), color='red', linestyle='--', linewidth=2, label=f'平均分: {self.df["总分"].mean():.1f}')
        ax.set_xlabel('成绩', fontsize=12)
        ax.set_ylabel('人数', fontsize=12)
        ax.set_title(f'{self.class_name} - 成绩分布直方图', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/1_成绩分布直方图.png', dpi=300)
        plt.close()
        
        # Plotly交互式版本
        fig_plotly = px.histogram(self.df, x='总分', nbins=20, title=f'{self.class_name} - 成绩分布直方图')
        fig_plotly.add_vline(x=self.df['总分'].mean(), line_dash="dash", line_color="red", 
                            annotation_text=f"平均分: {self.df['总分'].mean():.1f}")
        fig_plotly.write_html(f'{self.output_dir}/charts/1_成绩分布直方图_interactive.html')
        
        print("✅ 图表1: 成绩分布直方图")
    
    def plot_2_boxplot(self):
        """2. 成绩分布箱线图"""
        fig, ax = plt.subplots(figsize=(10, 6))
        box = ax.boxplot(self.df['总分'], patch_artist=True)
        box['boxes'][0].set_facecolor('#3498db')
        ax.set_ylabel('成绩', fontsize=12)
        ax.set_title(f'{self.class_name} - 成绩分布箱线图', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/2_成绩分布箱线图.png', dpi=300)
        plt.close()
        
        print("✅ 图表2: 成绩分布箱线图")
    
    def plot_3_violin(self):
        """3. 成绩分布小提琴图"""
        fig, ax = plt.subplots(figsize=(10, 6))
        parts = ax.violinplot(self.df['总分'], positions=[1], showmeans=True, showmedians=True)
        for pc in parts['bodies']:
            pc.set_facecolor('#3498db')
            pc.set_alpha(0.7)
        ax.set_xlabel('成绩分布', fontsize=12)
        ax.set_ylabel('成绩', fontsize=12)
        ax.set_title(f'{self.class_name} - 成绩分布小提琴图', fontsize=14, fontweight='bold')
        ax.set_xticks([])
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/3_成绩分布小提琴图.png', dpi=300)
        plt.close()
        
        print("✅ 图表3: 成绩分布小提琴图")
    
    def plot_4_pie(self):
        """4. 分数段分布饼图"""
        # 定义分数段
        bins = [0, 60, 70, 80, 90, 100]
        labels = ['不及格(<60)', '及格(60-69)', '中等(70-79)', '良好(80-89)', '优秀(90-100)']
        self.df['分数段'] = pd.cut(self.df['总分'], bins=bins, labels=labels, right=False)
        
        score_dist = self.df['分数段'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71', '#27ae60']
        wedges, texts, autotexts = ax.pie(score_dist.values, labels=score_dist.index, 
                                         autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title(f'{self.class_name} - 分数段分布饼图', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/4_分数段分布饼图.png', dpi=300)
        plt.close()
        
        print("✅ 图表4: 分数段分布饼图")
    
    def plot_5_cumulative(self):
        """5. 累计分布图"""
        sorted_scores = np.sort(self.df['总分'])
        cumulative = np.arange(1, len(sorted_scores) + 1) / len(sorted_scores)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(sorted_scores, cumulative * 100, linewidth=2, color='#3498db')
        ax.axhline(50, color='red', linestyle='--', alpha=0.5, label='50%分位数')
        ax.axvline(np.median(self.df['总分']), color='red', linestyle='--', alpha=0.5)
        ax.set_xlabel('成绩', fontsize=12)
        ax.set_ylabel('累计百分比 (%)', fontsize=12)
        ax.set_title(f'{self.class_name} - 成绩累计分布图', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        ax.legend()
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/5_成绩累计分布图.png', dpi=300)
        plt.close()
        
        print("✅ 图表5: 成绩累计分布图")
    
    def plot_6_question_bar(self):
        """6. 各题得分率柱状图"""
        question_names = list(self.results['question_stats'].keys())
        score_rates = [self.results['question_stats'][q]['得分率'] for q in question_names]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(range(len(question_names)), score_rates, color='#3498db', alpha=0.7)
        ax.axhline(60, color='red', linestyle='--', label='及格线(60%)')
        ax.set_xlabel('题目', fontsize=12)
        ax.set_ylabel('得分率 (%)', fontsize=12)
        ax.set_title(f'{self.class_name} - 各题得分率柱状图', fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(question_names)))
        ax.set_xticklabels(question_names, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # 添加数值标签
        for bar, rate in zip(bars, score_rates):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{rate:.1f}%', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/6_各题得分率柱状图.png', dpi=300)
        plt.close()
        
        print("✅ 图表6: 各题得分率柱状图")
    
    def plot_7_difficulty_scatter(self):
        """7. 各题难度散点图"""
        questions = list(self.results['question_stats'].keys())
        difficulties = [self.results['question_stats'][q]['难度'] for q in questions]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(range(len(questions)), difficulties, s=100, color='#e74c3c', alpha=0.7)
        ax.axhline(0.5, color='green', linestyle='--', label='中等难度(0.5)')
        ax.set_xlabel('题目', fontsize=12)
        ax.set_ylabel('难度系数', fontsize=12)
        ax.set_title(f'{self.class_name} - 各题难度散点图', fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(questions)))
        ax.set_xticklabels(questions, rotation=45, ha='right')
        ax.legend()
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/7_各题难度散点图.png', dpi=300)
        plt.close()
        
        print("✅ 图表7: 各题难度散点图")
    
    def plot_8_discrimination_scatter(self):
        """8. 各题区分度散点图"""
        questions = list(self.results['question_stats'].keys())
        discriminations = [self.results['question_stats'][q]['区分度'] for q in questions]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(range(len(questions)), discriminations, s=100, color='#2ecc71', alpha=0.7)
        ax.axhline(0.3, color='orange', linestyle='--', label='良好区分度(0.3)')
        ax.set_xlabel('题目', fontsize=12)
        ax.set_ylabel('区分度', fontsize=12)
        ax.set_title(f'{self.class_name} - 各题区分度散点图', fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(questions)))
        ax.set_xticklabels(questions, rotation=45, ha='right')
        ax.legend()
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/8_各题区分度散点图.png', dpi=300)
        plt.close()
        
        print("✅ 图表8: 各题区分度散点图")
    
    def plot_9_correlation_heatmap(self):
        """9. 题目相关性热力图"""
        corr_matrix = self.df[self.score_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, ax=ax, cbar_kws={'label': '相关系数'})
        ax.set_title(f'{self.class_name} - 题目相关性热力图', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/9_题目相关性热力图.png', dpi=300)
        plt.close()
        
        print("✅ 图表9: 题目相关性热力图")
    
    def plot_10_radar(self):
        """10. 班级对比雷达图（如果有多个班级）"""
        # 这里简化为展示各题得分率的雷达图
        question_names = list(self.results['question_stats'].keys())[:8]  # 取前8题
        score_rates = [self.results['question_stats'][q]['得分率'] for q in question_names]
        
        # 闭合雷达图
        question_names.append(question_names[0])
        score_rates.append(score_rates[0])
        
        angles = np.linspace(0, 2 * np.pi, len(question_names), endpoint=False).tolist()
        score_rates = score_rates
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        ax.plot(angles, score_rates, 'o-', linewidth=2, color='#3498db')
        ax.fill(angles, score_rates, alpha=0.25, color='#3498db')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(question_names[:-1])
        ax.set_ylim(0, 100)
        ax.set_title(f'{self.class_name} - 各题得分率雷达图', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/10_各题得分率雷达图.png', dpi=300)
        plt.close()
        
        print("✅ 图表10: 各题得分率雷达图")
    
    def plot_11_qq(self):
        """11. Q-Q图（检验正态分布）"""
        fig, ax = plt.subplots(figsize=(10, 6))
        stats.probplot(self.df['总分'], dist="norm", plot=ax)
        ax.set_title(f'{self.class_name} - 成绩Q-Q图（正态分布检验）', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/11_成绩QQ图.png', dpi=300)
        plt.close()
        
        print("✅ 图表11: 成绩Q-Q图")
    
    def plot_12_score_heatmap(self):
        """12. 题目得分率热力图（学生×题目）"""
        # 取前20名学生和所有题目
        n_students = min(20, len(self.df))
        sample_df = self.df.sample(n=n_students, random_state=42)
        
        # 计算每题得分率
        score_rate_df = sample_df[self.score_cols].div(self.df[self.score_cols].max())
        
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(score_rate_df, annot=False, cmap='YlOrRd', 
                   cbar_kws={'label': '得分率'}, ax=ax)
        ax.set_xlabel('题目', fontsize=12)
        ax.set_ylabel('学生', fontsize=12)
        ax.set_title(f'{self.class_name} - 学生×题目得分热力图（样本）', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/12_学生题目得分热力图.png', dpi=300)
        plt.close()
        
        print("✅ 图表12: 学生×题目得分热力图")
    
    def plot_13_difficulty_discrimination(self):
        """13. 难度-区分度四象限图"""
        questions = list(self.results['question_stats'].keys())
        difficulties = [self.results['question_stats'][q]['难度'] for q in questions]
        discriminations = [self.results['question_stats'][q]['区分度'] for q in questions]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        scatter = ax.scatter(difficulties, discriminations, s=100, alpha=0.7, c=range(len(questions)), cmap='viridis')
        
        # 添加题目标签
        for i, q in enumerate(questions):
            ax.annotate(q, (difficulties[i], discriminations[i]), fontsize=8)
        
        ax.axvline(0.5, color='gray', linestyle='--', alpha=0.5)
        ax.axhline(0.3, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlabel('难度系数', fontsize=12)
        ax.set_ylabel('区分度', fontsize=12)
        ax.set_title(f'{self.class_name} - 难度-区分度四象限图', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        plt.colorbar(scatter, ax=ax, label='题目序号')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/13_难度区分度四象限图.png', dpi=300)
        plt.close()
        
        print("✅ 图表13: 难度-区分度四象限图")
    
    def plot_14_boxplot_questions(self):
        """14. 各题得分率分布箱线图"""
        score_rates = []
        labels = []
        for col in self.score_cols:
            max_score = self.df[col].max()
            if max_score > 0:
                rate = self.df[col] / max_score * 100
                score_rates.append(rate)
                labels.append(col)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.boxplot(score_rates, labels=labels, patch_artist=True)
        ax.set_xlabel('题目', fontsize=12)
        ax.set_ylabel('得分率 (%)', fontsize=12)
        ax.set_title(f'{self.class_name} - 各题得分率分布箱线图', fontsize=14, fontweight='bold')
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/14_各题得分率分布箱线图.png', dpi=300)
        plt.close()
        
        print("✅ 图表14: 各题得分率分布箱线图")
    
    def plot_15_ranking_scatter(self):
        """15. 成绩排名散点图"""
        rankings = range(1, len(self.df) + 1)
        scores = self.df['总分'].sort_values(ascending=False).values
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(rankings, scores, s=50, alpha=0.7, color='#3498db')
        ax.axhline(self.df['总分'].mean(), color='red', linestyle='--', label=f'平均分: {self.df["总分"].mean():.1f}')
        ax.set_xlabel('排名', fontsize=12)
        ax.set_ylabel('成绩', fontsize=12)
        ax.set_title(f'{self.class_name} - 成绩排名散点图', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/15_成绩排名散点图.png', dpi=300)
        plt.close()
        
        print("✅ 图表15: 成绩排名散点图")
    
    def plot_16_outliers(self):
        """16. 异常值检测图"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 使用箱线图检测异常值
        box = ax.boxplot(self.df['总分'], patch_artist=True)
        outliers = [y for y in self.df['总分'] if y < box['whiskers'][0].get_ydata()[0] or 
                   y > box['whiskers'][1].get_ydata()[0]]
        
        ax.set_ylabel('成绩', fontsize=12)
        ax.set_title(f'{self.class_name} - 异常值检测图（共{len(outliers)}个异常值）', fontsize=14, fontweight='bold')
        ax.set_xticks([])
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/16_异常值检测图.png', dpi=300)
        plt.close()
        
        print("✅ 图表16: 异常值检测图")
    
    def plot_17_pass_excellent_bar(self):
        """17. 及格率/优秀率柱状图"""
        # 按分数段统计
        bins = [0, 60, 70, 80, 90, 100]
        labels = ['不及格', '及格', '中等', '良好', '优秀']
        self.df['等级'] = pd.cut(self.df['总分'], bins=bins, labels=labels, right=False)
        grade_counts = self.df['等级'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71', '#27ae60']
        bars = ax.bar(grade_counts.index, grade_counts.values, color=colors, alpha=0.7)
        ax.set_xlabel('等级', fontsize=12)
        ax.set_ylabel('人数', fontsize=12)
        ax.set_title(f'{self.class_name} - 各等级人数分布', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=11)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/17_各等级人数分布.png', dpi=300)
        plt.close()
        
        print("✅ 图表17: 各等级人数分布")
    
    def plot_18_3d_histogram(self):
        """18. 成绩分布3D直方图"""
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # 创建3D直方图数据
        x = self.df['总分']
        y = np.zeros_like(x)
        hist, x_edges, y_edges = np.histogram2d(x, y, bins=[20, 1])
        
        # 绘制3D柱状图
        x_pos, y_pos = np.meshgrid(x_edges[:-1], y_edges[:-1])
        x_pos = x_pos.flatten()
        y_pos = y_pos.flatten()
        z_pos = np.zeros_like(x_pos)
        
        dx = (x_edges[1] - x_edges[0]) * np.ones_like(x_pos)
        dy = (y_edges[1] - y_edges[0]) * np.ones_like(y_pos)
        dz = hist.flatten()
        
        ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color='#3498db', alpha=0.7)
        ax.set_xlabel('成绩', fontsize=12)
        ax.set_ylabel('', fontsize=12)
        ax.set_zlabel('人数', fontsize=12)
        ax.set_title(f'{self.class_name} - 成绩分布3D直方图', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/18_成绩分布3D直方图.png', dpi=300)
        plt.close()
        
        print("✅ 图表18: 成绩分布3D直方图")
    
    def plot_19_area(self):
        """19. 成绩分布面积图"""
        sorted_scores = np.sort(self.df['总分'])
        cumulative = np.arange(1, len(sorted_scores) + 1) / len(sorted_scores) * 100
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.fill_between(sorted_scores, cumulative, alpha=0.3, color='#3498db')
        ax.plot(sorted_scores, cumulative, linewidth=2, color='#3498db')
        ax.set_xlabel('成绩', fontsize=12)
        ax.set_ylabel('累计百分比 (%)', fontsize=12)
        ax.set_title(f'{self.class_name} - 成绩分布面积图', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/19_成绩分布面积图.png', dpi=300)
        plt.close()
        
        print("✅ 图表19: 成绩分布面积图")
    
    def plot_20_horizontal_bar(self):
        """20. 各题得分率横向柱状图"""
        question_names = list(self.results['question_stats'].keys())
        score_rates = [self.results['question_stats'][q]['得分率'] for q in question_names]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(range(len(question_names)), score_rates, color='#3498db', alpha=0.7)
        ax.axvline(60, color='red', linestyle='--', label='及格线(60%)')
        ax.set_xlabel('得分率 (%)', fontsize=12)
        ax.set_ylabel('题目', fontsize=12)
        ax.set_title(f'{self.class_name} - 各题得分率横向柱状图', fontsize=14, fontweight='bold')
        ax.set_yticks(range(len(question_names)))
        ax.set_yticklabels(question_names)
        ax.legend()
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/20_各题得分率横向柱状图.png', dpi=300)
        plt.close()
        
        print("✅ 图表20: 各题得分率横向柱状图")
    
    def plot_21_reliability(self):
        """21. 信度分析图"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 模拟信度系数
        alpha = self.results.get('reliability', 0)
        
        # 绘制信度仪表盘
        categories = ['极低', '低', '可接受', '良好', '优秀']
        thresholds = [0, 0.5, 0.6, 0.7, 0.8, 1.0]
        colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60']
        
        # 找到当前信度所在区间
        for i in range(len(thresholds)-1):
            if thresholds[i] <= alpha < thresholds[i+1]:
                current_category = categories[i]
                current_color = colors[i]
                break
        else:
            current_category = '优秀'
            current_color = colors[-1]
        
        ax.barh(0, alpha, color=current_color, height=0.5)
        ax.axvline(0.6, color='gray', linestyle='--', alpha=0.5, label='可接受阈值(0.6)')
        ax.axvline(0.8, color='gray', linestyle='--', alpha=0.5, label='优秀阈值(0.8)')
        ax.set_xlabel('Cronbach\'s α系数', fontsize=12)
        ax.set_title(f'{self.class_name} - 信度分析图 (α={alpha:.3f}, {current_category})', 
                    fontsize=14, fontweight='bold')
        ax.set_yticks([])
        ax.set_xlim(0, 1)
        ax.legend()
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/21_信度分析图.png', dpi=300)
        plt.close()
        
        print("✅ 图表21: 信度分析图")
    
    def plot_22_waterfall(self):
        """22. 得分率瀑布图"""
        question_names = list(self.results['question_stats'].keys())
        score_rates = [self.results['question_stats'][q]['得分率'] for q in question_names]
        
        # 计算累计得分率
        cumulative = np.cumsum(score_rates)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 绘制瀑布图
        for i in range(len(question_names)):
            if i == 0:
                ax.bar(i, score_rates[i], bottom=0, color='#3498db', alpha=0.7)
            else:
                ax.bar(i, score_rates[i], bottom=cumulative[i-1], color='#3498db', alpha=0.7)
        
        ax.set_xlabel('题目', fontsize=12)
        ax.set_ylabel('累计得分率 (%)', fontsize=12)
        ax.set_title(f'{self.class_name} - 各题得分率瀑布图', fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(question_names)))
        ax.set_xticklabels(question_names, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/charts/22_各题得分率瀑布图.png', dpi=300)
        plt.close()
        
        print("✅ 图表22: 各题得分率瀑布图")
    
    # ==================== 生成所有图表 ====================
    
    def generate_all_charts(self):
        """生成所有22种可视化图表"""
        print("\n🎨 开始生成可视化图表...\n")
        
        # 计算统计数据
        self.calculate_statistics()
        self.calculate_reliability()
        
        # 生成所有图表
        self.plot_1_histogram()
        self.plot_2_boxplot()
        self.plot_3_violin()
        self.plot_4_pie()
        self.plot_5_cumulative()
        self.plot_6_question_bar()
        self.plot_7_difficulty_scatter()
        self.plot_8_discrimination_scatter()
        self.plot_9_correlation_heatmap()
        self.plot_10_radar()
        self.plot_11_qq()
        self.plot_12_score_heatmap()
        self.plot_13_difficulty_discrimination()
        self.plot_14_boxplot_questions()
        self.plot_15_ranking_scatter()
        self.plot_16_outliers()
        self.plot_17_pass_excellent_bar()
        self.plot_18_3d_histogram()
        self.plot_19_area()
        self.plot_20_horizontal_bar()
        self.plot_21_reliability()
        self.plot_22_waterfall()
        
        print(f"\n✅ 所有图表生成完成！共22种可视化图表")
        print(f"📁 输出目录：{self.output_dir}/charts/")
    
    # ==================== 生成分析报告 ====================
    
    def generate_report(self):
        """生成分析报告（Markdown格式）"""
        report_path = f'{self.output_dir}/分析报告.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# {self.class_name} - 期末试卷分析报告\n\n")
            f.write(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"---\n\n")
            
            # 1. 成绩概览
            f.write("## 📊 一、成绩概览\n\n")
            f.write("| 指标 | 数值 |\n")
            f.write("|------|------|\n")
            for key, value in self.results['basic_stats'].items():
                if isinstance(value, float):
                    f.write(f"| {key} | {value:.2f} |\n")
                else:
                    f.write(f"| {key} | {value} |\n")
            f.write("\n")
            
            # 2. 题目分析
            f.write("## 📝 二、题目分析\n\n")
            f.write("| 题目 | 得分率(%) | 难度系数 | 区分度 |\n")
            f.write("|------|-----------|----------|--------|\n")
            for q, stats in self.results['question_stats'].items():
                f.write(f"| {q} | {stats['得分率']:.1f} | {stats['难度']:.3f} | {stats['区分度']:.3f} |\n")
            f.write("\n")
            
            # 3. 信度分析
            f.write("## 🔍 三、信度分析\n\n")
            f.write(f"- **Cronbach's α系数**：{self.results.get('reliability', 0):.3f}\n")
            if self.results.get('reliability', 0) >= 0.8:
                f.write("- **评价**：信度优秀，试卷一致性很高\n")
            elif self.results.get('reliability', 0) >= 0.7:
                f.write("- **评价**：信度良好，试卷一致性较好\n")
            elif self.results.get('reliability', 0) >= 0.6:
                f.write("- **评价**：信度可接受，建议优化部分题目\n")
            else:
                f.write("- **评价**：信度较低，建议重新设计试卷\n")
            f.write("\n")
            
            # 4. 教学建议
            f.write("## 💡 四、教学建议\n\n")
            f.write("基于本次试卷分析结果，提出以下教学改进建议：\n\n")
            
            # 找出得分率低的题目
            low_score_questions = [q for q, s in self.results['question_stats'].items() if s['得分率'] < 60]
            if low_score_questions:
                f.write(f"1. **重点讲解内容**：以下题目得分率较低，需要在教学中加强讲解：{', '.join(low_score_questions)}\n\n")
            
            # 找出区分度低的题目
            low_disc_questions = [q for q, s in self.results['question_stats'].items() if s['区分度'] < 0.3]
            if low_disc_questions:
                f.write(f"2. **题目优化建议**：以下题目区分度较低，建议优化题目设计：{', '.join(low_disc_questions)}\n\n")
            
            f.write("3. **整体教学策略**：根据学生答题情况调整教学进度和方法\n\n")
            f.write("\n---\n\n")
            f.write("*本报告由 WorkBuddy 期末试卷分析仪表盘自动生成*\n")
        
        print(f"✅ 分析报告已生成：{report_path}")
    
    # ==================== 生成公众号推文 ====================
    
    def generate_wechat_article(self):
        """生成公众号推文HTML"""
        html_path = f'{self.output_dir}/公众号推文.html'
        
        # 读取图表文件
        chart_files = sorted([f for f in os.listdir(f'{self.output_dir}/charts') if f.endswith('.png')])
        
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.class_name} - 期末试卷分析报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            line-height: 1.8;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .section {{
            background: white;
            padding: 30px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            font-size: 22px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            color: #333;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-card .label {{
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 5px;
        }}
        .stat-card .value {{
            font-size: 28px;
            font-weight: bold;
        }}
        .chart-container {{
            margin: 30px 0;
            text-align: center;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .chart-container .caption {{
            margin-top: 10px;
            color: #666;
            font-size: 14px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        table th, table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        table th {{
            background-color: #667eea;
            color: white;
        }}
        .suggestion {{
            background: #f8f9fa;
            padding: 20px;
            border-left: 4px solid #667eea;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
        }}
        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 {self.class_name}</h1>
        <p>期末试卷深度分析报告</p>
        <p>生成时间：{datetime.now().strftime('%Y年%m月%d日')}</p>
    </div>
    
    <div class="section">
        <h2>📈 一、成绩概览</h2>
        <div class="stats-grid">
"""
        
        # 添加统计卡片
        for key, value in self.results['basic_stats'].items():
            if isinstance(value, float):
                value_str = f"{value:.1f}"
            else:
                value_str = str(value)
            html_content += f"""
            <div class="stat-card">
                <div class="label">{key}</div>
                <div class="value">{value_str}</div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
    
    <div class="section">
        <h2>📊 二、可视化分析</h2>
"""
        
        # 添加图表
        chart_names = {
            '1_成绩分布直方图.png': '成绩分布直方图',
            '2_成绩分布箱线图.png': '成绩分布箱线图',
            '3_成绩分布小提琴图.png': '成绩分布小提琴图',
            '4_分数段分布饼图.png': '分数段分布',
            '5_成绩累计分布图.png': '成绩累计分布',
            '6_各题得分率柱状图.png': '各题得分率',
            '7_各题难度散点图.png': '题目难度分析',
            '8_各题区分度散点图.png': '题目区分度分析',
            '9_题目相关性热力图.png': '题目相关性',
            '10_各题得分率雷达图.png': '各题得分率雷达图',
            '13_难度区分度四象限图.png': '题目质量分析',
            '17_各等级人数分布.png': '各等级人数分布',
        }
        
        for chart_file in chart_files[:12]:  # 只显示前12个图表
            if chart_file in chart_names:
                html_content += f"""
        <div class="chart-container">
            <img src="charts/{chart_file}" alt="{chart_names[chart_file]}">
            <div class="caption">{chart_names[chart_file]}</div>
        </div>
"""
        
        html_content += """
    </div>
    
    <div class="section">
        <h2>📝 三、题目分析</h2>
        <table>
            <tr>
                <th>题目</th>
                <th>得分率(%)</th>
                <th>难度系数</th>
                <th>区分度</th>
                <th>评价</th>
            </tr>
"""
        
        # 添加题目分析表格
        for q, stats in self.results['question_stats'].items():
            if stats['得分率'] >= 80:
                evaluation = "简单"
            elif stats['得分率'] >= 60:
                evaluation = "适中"
            else:
                evaluation = "偏难"
            
            html_content += f"""
            <tr>
                <td>{q}</td>
                <td>{stats['得分率']:.1f}</td>
                <td>{stats['难度']:.3f}</td>
                <td>{stats['区分度']:.3f}</td>
                <td>{evaluation}</td>
            </tr>
"""
        
        html_content += """
        </table>
    </div>
    
    <div class="section">
        <h2>💡 四、教学建议</h2>
"""
        
        # 添加教学建议
        low_score_questions = [q for q, s in self.results['question_stats'].items() if s['得分率'] < 60]
        if low_score_questions:
            html_content += f"""
        <div class="suggestion">
            <strong>📌 重点讲解内容：</strong><br>
            以下题目得分率较低，需要在教学中加强讲解：{', '.join(low_score_questions)}
        </div>
"""
        
        low_disc_questions = [q for q, s in self.results['question_stats'].items() if s['区分度'] < 0.3]
        if low_disc_questions:
            html_content += f"""
        <div class="suggestion">
            <strong>📌 题目优化建议：</strong><br>
            以下题目区分度较低，建议优化题目设计：{', '.join(low_disc_questions)}
        </div>
"""
        
        html_content += """
        <div class="suggestion">
            <strong>📌 整体教学策略：</strong><br>
            根据学生答题情况调整教学进度和方法，注重基础知识的巩固和综合能力的提升。
        </div>
    </div>
    
    <div class="footer">
        <p>📊 本报告由 <strong>WorkBuddy 期末试卷分析仪表盘</strong> 自动生成</p>
        <p>💼  powered by WorkBuddy - AI赋能教育教学</p>
    </div>
</body>
</html>
"""
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 公众号推文已生成：{html_path}")
        print(f"💡 提示：可直接在浏览器中打开查看，或复制HTML代码到微信公众号平台")
    
    # ==================== 主流程 ====================
    
    def run_analysis(self):
        """运行完整分析流程"""
        print("="*60)
        print(f"🎓 {self.class_name} - 期末试卷分析仪表盘")
        print("="*60)
        print()
        
        # 1. 生成所有图表
        self.generate_all_charts()
        
        # 2. 生成分析报告
        self.generate_report()
        
        # 3. 生成公众号推文
        self.generate_wechat_article()
        
        print("\n" + "="*60)
        print("✅ 分析完成！")
        print("="*60)
        print(f"\n📁 输出目录：{self.output_dir}/")
        print(f"   - 22种可视化图表：{self.output_dir}/charts/")
        print(f"   - 分析报告：{self.output_dir}/分析报告.md")
        print(f"   - 公众号推文：{self.output_dir}/公众号推文.html")
        print("\n💡 提示：")
        print("   1. 可在浏览器中打开 '公众号推文.html' 查看效果")
        print("   2. 可将HTML代码复制到微信公众号平台直接发布")
        print("   3. 所有图表已保存为高清PNG格式，可插入PPT或报告")
        print()


# ==================== 命令行入口 ====================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python exam_analyzer.py <数据文件路径> [班级名称]")
        print("示例：python exam_analyzer.py data.xlsx '网络与新媒体2301班'")
        sys.exit(1)
    
    data_path = sys.argv[1]
    class_name = sys.argv[2] if len(sys.argv) > 2 else "未知班级"
    
    # 创建分析器并运行
    analyzer = ExamAnalyzer(data_path, class_name)
    analyzer.run_analysis()
