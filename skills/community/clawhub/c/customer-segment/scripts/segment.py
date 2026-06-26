#!/usr/bin/env python3
"""
客户分群分析脚本
用法: python segment.py <客户数据.csv> [输出目录]
"""

import sys
import os
import json
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ── 标签体系 ──────────────────────────────────────────────
CLUSTER_LABELS = {
    0: ("🌟 高价值客户",    "VIP / 高净值客户，重点维护"),
    1: ("⬆️ 潜力客户",      "成长型，有转化潜力"),
    2: ("🟢 稳定客户",      "中低频，低风险"),
    3: ("🔄 活跃交易客户",  "交易频繁，佣金贡献高"),
    4: ("⚠️ 流失预警",      "活跃度下降，需激活"),
}
FALLBACK_LABELS = {
    i: (f"客户群体 {i}", "") for i in range(100)
}

# ── 特征工程 ─────────────────────────────────────────────
FEATURE_COLS = [
    'recency',      # 越活跃越小
    'frequency',    # 越多越好
    'monetary',     # 越高越好
    'balance',      # 资产余额
    'tenure',       # 持有时长（月）
    'product_depth',# 持有产品数
    'age',          # 年龄
]


def load_and_clean(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    raw_cols = list(df.columns)

    # 自动识别列名映射
    col_map = {}
    for col in raw_cols:
        cl = col.lower()
        if 'id' in cl:              col_map[col] = 'customer_id'
        elif 'balance' in cl:       col_map[col] = 'balance'
        elif 'amount' in cl and 'txn' in cl: col_map[col] = 'monetary'
        elif 'count' in cl and 'txn' in cl: col_map[col] = 'frequency'
        elif 'date' in cl and 'last' in cl: col_map[col] = 'last_date'
        elif 'date' in cl and 'open' in cl: col_map[col] = 'open_date'
        elif 'product' in cl and 'count' in cl: col_map[col] = 'product_depth'
        elif 'age' in cl:           col_map[col] = 'age'
        elif 'gender' in cl:         col_map[col] = 'gender'
        elif 'txn' in cl:            col_map[col] = 'monetary'
    df.rename(columns=col_map, inplace=True)

    today = pd.Timestamp.today()

    # RFM
    if 'last_date' in df.columns:
        df['last_date'] = pd.to_datetime(df['last_date'], errors='coerce')
        df['recency'] = (today - df['last_date']).dt.days.clip(lower=0)
    else:
        df['recency'] = df.get('recency', 180)

    if 'frequency' not in df.columns:
        df['frequency'] = 1
    df['frequency'] = pd.to_numeric(df['frequency'], errors='coerce').fillna(1)

    if 'monetary' not in df.columns:
        df['monetary'] = df.get('balance', 0)
    df['monetary'] = pd.to_numeric(df['monetary'], errors='coerce').fillna(0)

    if 'balance' not in df.columns:
        df['balance'] = df['monetary']
    df['balance'] = pd.to_numeric(df['balance'], errors='coerce').fillna(0)

    if 'open_date' in df.columns:
        df['open_date'] = pd.to_datetime(df['open_date'], errors='coerce')
        df['tenure'] = ((today - df['open_date']).dt.days / 30).clip(lower=0)
    else:
        df['tenure'] = 12  # 默认

    if 'product_depth' not in df.columns:
        df['product_depth'] = 1
    df['product_depth'] = pd.to_numeric(df['product_depth'], errors='coerce').fillna(1)

    if 'age' not in df.columns:
        df['age'] = 40
    df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(40)

    # 数值列缺失值填充
    num_cols = ['recency', 'frequency', 'monetary', 'balance', 'tenure', 'product_depth', 'age']
    for c in num_cols:
        if c in df.columns:
            df[c] = df[c].fillna(df[c].median())

    return df


def build_features(df):
    feats = df[FEATURE_COLS].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(feats)
    return X_scaled, feats, scaler


def find_optimal_k(X_scaled, max_k=8):
    scores = {}
    for k in range(2, max_k + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        scores[k] = {
            'sse': km.inertia_,
            'sil': silhouette_score(X_scaled, labels),
            'db':  davies_bouldin_score(X_scaled, labels),
        }
    best_k = max(scores, key=lambda k: scores[k]['sil'])
    return best_k, scores


def cluster(df, X_scaled, n_clusters=5):
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['cluster'] = km.fit_predict(X_scaled)
    return km, df


def label_clusters(df):
    """按 balance 中位数排序，给簇打标签"""
    med = df.groupby('cluster')['balance'].median().sort_values(ascending=False)
    rank = {c: i for i, c in enumerate(med.index)}
    df['cluster_rank'] = df['cluster'].map(rank)
    n = df['cluster'].nunique()
    labels = list(CLUSTER_LABELS.values())[:n] + list(FALLBACK_LABELS.values())[n:]
    label_map = {orig: labels[rank[orig]] for orig in rank}
    df['segment_label'] = df['cluster'].map(lambda c: label_map.get(c, (f"群体{c}", ""))[0])
    df['segment_desc']  = df['cluster'].map(lambda c: label_map.get(c, ("", ""))[1])
    return df


def make_charts(df, feats, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, 'segmentation_charts.png')
    n_clusters = df['cluster'].nunique()

    fig, axes = plt.subplots(2, 2, figsize=(14, 11))

    # 1. 资产分布
    colors = plt.cm.Set2(np.linspace(0, 1, n_clusters))
    for c in sorted(df['cluster'].unique()):
        sub = df[df['cluster'] == c]['balance'].dropna()
        axes[0,0].hist(sub, bins=25, alpha=0.6, label=f'C{c}', color=colors[c])
    axes[0,0].set_xlabel('Balance (Asset)')
    axes[0,0].set_ylabel('Count')
    axes[0,0].set_title('Asset Distribution by Cluster')
    axes[0,0].legend(fontsize=8)
    axes[0,0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    # 2. 分群特征雷达图
    cluster_means = feats.groupby(df['cluster']).mean()
    cluster_means_norm = (cluster_means - cluster_means.min()) / (cluster_means.max() - cluster_means.min() + 1e-9)
    cats = list(cluster_means.columns)
    N = len(cats)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    ax_radar = axes[0,1]
    ax_radar = plt.subplot(2, 2, 2, polar=True)
    for c in sorted(df['cluster'].unique()):
        vals = list(cluster_means_norm.loc[c]) + [cluster_means_norm.loc[c][0]]
        ax_radar.plot(angles, vals, 'o-', linewidth=2, label=f'C{c}', color=colors[c])
        ax_radar.fill(angles, vals, alpha=0.1, color=colors[c])
    ax_radar.set_xticks(angles[:-1])
    ax_radar.set_xticklabels(cats, fontsize=8)
    ax_radar.set_title('Cluster Feature Radar', pad=20)
    ax_radar.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=7)

    # 3. 热力图
    im = axes[1,0].imshow(cluster_means_norm.T, cmap='YlOrRd', aspect='auto')
    axes[1,0].set_xticks(range(n_clusters))
    axes[1,0].set_xticklabels([f'C{i}' for i in range(n_clusters)])
    axes[1,0].set_yticks(range(len(cats)))
    axes[1,0].set_yticklabels(cats, fontsize=8)
    axes[1,0].set_title('Cluster Feature Heatmap (Normalized)')
    plt.colorbar(im, ax=axes[1,0], shrink=0.8)

    # 4. 散点图
    for c in sorted(df['cluster'].unique()):
        sub = df[df['cluster'] == c]
        axes[1,1].scatter(sub['frequency'], sub['balance'],
                           alpha=0.5, s=10, label=f'C{c}', color=colors[c])
    axes[1,1].set_xlabel('Frequency (txn count)')
    axes[1,1].set_ylabel('Balance')
    axes[1,1].set_title('Frequency vs Balance by Cluster')
    axes[1,1].legend(fontsize=7)
    axes[1,1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.suptitle('Customer Segmentation Analysis', fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    return path


def summarize(df, scores, best_k, output_dir):
    summary = df.groupby(['cluster', 'segment_label']).agg({
        'balance':    ['mean', 'median', 'count'],
        'frequency':  'mean',
        'monetary':   'mean',
        'recency':    'mean',
        'tenure':     'mean',
        'product_depth': 'mean',
        'age':        'mean',
    }).round(2)
    summary.columns = ['_'.join(c) for c in summary.columns]

    report = f"""# 客户分群分析报告

## 基本信息
- 分析时间: {pd.Timestamp.today().strftime('%Y-%m-%d')}
- 客户总数: {len(df)}
- 最优分群数: {best_k}（轮廓系数: {scores[best_k]['sil']:.3f}）

## 各分群概况

| 簇 | 标签 | 人数 | 平均资产 | 中位资产 | 平均交易频次 | 平均最近交易(天) |
|----|------|------|----------|----------|--------------|----------------|
"""
    for c in sorted(df['cluster'].unique()):
        row = df[df['cluster'] == c]
        label = row['segment_label'].iloc[0]
        report += f"| C{c} | {label} | {len(row)} | {row['balance'].mean():.0f} | {row['balance'].median():.0f} | {row['frequency'].mean():.1f} | {row['recency'].mean():.0f} |\n"

    report += f"""
## 分群特征雷达图 / 热力图

- 详细聚类参数说明见: `references/clustering-guide.md`
- RFM模型说明见: `references/rfm-guide.md`

## 分群策略建议

"""
    for c in sorted(df['cluster'].unique()):
        label = df[df['cluster']==c]['segment_label'].iloc[0]
        desc  = df[df['cluster']==c]['segment_desc'].iloc[0]
        avg_bal = df[df['cluster']==c]['balance'].mean()
        report += f"**C{c} {label}**：{desc}（平均资产 {avg_bal:.0f}）\n"

    rpt_path = os.path.join(output_dir, 'segmentation_report.md')
    with open(rpt_path, 'w', encoding='utf-8') as f:
        f.write(report)
    return rpt_path, summary


def main():
    input_path  = sys.argv[1] if len(sys.argv) > 1 else 'customers.csv'
    output_dir  = sys.argv[2] if len(sys.argv) > 2 else 'output'
    os.makedirs(output_dir, exist_ok=True)

    print(f"[1/5] Loading data: {input_path}")
    df = load_and_clean(input_path)
    print(f"      Loaded {len(df)} rows, columns: {list(df.columns)}")

    print(f"[2/5] Building features...")
    X_scaled, feats, scaler = build_features(df)

    print(f"[3/5] Finding optimal K...")
    best_k, scores = find_optimal_k(X_scaled)
    print(f"      Optimal K={best_k}  sil={scores[best_k]['sil']:.3f}  db={scores[best_k]['db']:.3f}")

    print(f"[4/5] Clustering into {best_k} groups...")
    km, df = cluster(df, X_scaled, n_clusters=best_k)
    df = label_clusters(df)

    print(f"[5/5] Generating charts and report...")
    chart_path = make_charts(df, feats, output_dir)
    rpt_path, summary = summarize(df, scores, best_k, output_dir)

    # 保存结果
    out_csv = os.path.join(output_dir, 'segmentation_results.csv')
    df.to_csv(out_csv, index=False, encoding='utf-8-sig')

    sum_csv = os.path.join(output_dir, 'cluster_summary.csv')
    summary.to_csv(sum_csv, encoding='utf-8-sig')

    print(f"""
✅ 分群完成！

输出文件：
  📊 分群结果   → {out_csv}
  📋 分群汇总   → {sum_csv}
  📈 可视化图表 → {chart_path}
  📝 分析报告   → {rpt_path}

各分群人数：
{df['segment_label'].value_counts().to_string()}
""")

    return df, scores, best_k


if __name__ == '__main__':
    main()
