"""
PCA主成分分析模块

通用功能：标准化 → PCA降维 → 碎石图 → 2D/3D散点图 → 一致性评价。
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import preprocessing


def pca_analyze(df, variance_threshold=0.95, n_components=None):
    """
    完整PCA分析流程。
    
    Parameters
    ----------
    df : pd.DataFrame
        原始数据（行为样本，列为变量）
    variance_threshold : float
        累积贡献率阈值（默认0.95）
    n_components : int, optional
        指定主成分数量（优先于variance_threshold）
    
    Returns
    -------
    dict
        {
            "pca_model": PCA对象,
            "transformed": 降维后数据,
            "components": 主成分载荷矩阵,
            "explained_variance": 方差,
            "explained_ratio": 方差贡献率,
            "cumulative_ratio": 累积贡献率,
            "n_selected": 选取的主成分数,
        }
    """
    # 标准化
    scaler = preprocessing.StandardScaler()
    df_scaled = scaler.fit_transform(df)
    scaled_df = pd.DataFrame(df_scaled, columns=df.columns)
    
    # 先全部拟合以获取完整信息
    full_pca = PCA(n_components=min(df.shape[1], df.shape[0]))
    full_pca.fit(scaled_df)
    
    # 确定主成分数
    if n_components:
        k = n_components
    else:
        cumsum = np.cumsum(full_pca.explained_variance_ratio_)
        k = np.searchsorted(cumsum, variance_threshold) + 1
    
    k = min(k, full_pca.n_components_)
    
    # 最终PCA
    pca = PCA(n_components=k)
    transformed = pca.fit_transform(scaled_df)
    
    # 因子得分（标准化）
    scaler2 = preprocessing.StandardScaler()
    transformed_scaled = scaler2.fit_transform(transformed)
    sign = np.sign(pca.components_.sum(axis=1))
    factor_scores = transformed_scaled * sign
    
    # 成分得分系数矩阵
    component_scores = pca.components_ / np.sqrt(pca.explained_variance_.reshape(-1, 1))
    
    return {
        "pca_model": pca,
        "full_pca": full_pca,
        "transformed": pd.DataFrame(transformed, columns=[f"PC{i+1}" for i in range(k)]),
        "factor_scores": pd.DataFrame(factor_scores, columns=[f"F{i+1}" for i in range(k)]),
        "components": pd.DataFrame(pca.components_, columns=df.columns,
                                    index=[f"PC{i+1}" for i in range(k)]),
        "component_scores": pd.DataFrame(component_scores, columns=df.columns,
                                          index=[f"PC{i+1}" for i in range(k)]),
        "explained_variance": pca.explained_variance_,
        "explained_ratio": pca.explained_variance_ratio_,
        "cumulative_ratio": np.cumsum(pca.explained_variance_ratio_),
        "n_selected": k,
        "total_variance_explained": np.sum(pca.explained_variance_ratio_),
    }


def scree_plot(full_pca, threshold=0.95, highlight_k=None):
    """
    绘制碎石图（累积贡献率）。
    
    Parameters
    ----------
    full_pca : PCA
        拟合后的PCA对象（需包含全部分量）
    threshold : float
        累积贡献率阈值线
    highlight_k : int, optional
        高亮选定的主成分数
    
    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    x = range(1, len(full_pca.explained_variance_ratio_) + 1)
    y_cum = np.cumsum(full_pca.explained_variance_ratio_)
    y_remain = 1 - y_cum
    
    ax.plot(x, y_remain, color='#000000', marker='.', linestyle='-', linewidth=2, markersize=8)
    
    for i, (a, b, c) in enumerate(zip(x, y_remain, y_cum)):
        ax.text(a, b, f'{c:.1%}', ha='center', va='bottom', fontsize=8,
                color='#e74c3c' if highlight_k and i + 1 == highlight_k else '#333333')
    
    ax.axhline(1 - threshold, color='#FF0000', linestyle='--', linewidth=0.8,
               label=f'{threshold:.0%} 阈值')
    ax.set_title('碎石图 — 主成分累积贡献率', fontsize=14)
    ax.set_xlabel('主成分序号')
    ax.set_ylabel('1 - 累积贡献率')
    ax.legend(loc=1)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    return fig


def pca_scatter(pca_result, labels=None, dim=2):
    """
    主成分散点图（2D或3D）。
    
    Parameters
    ----------
    pca_result : dict
        pca_analyze 的返回结果
    labels : array-like, optional
        样本标签（用于着色）
    dim : int
        2 或 3
    
    Returns
    -------
    matplotlib.figure.Figure
    """
    scores = pca_result["factor_scores"]
    n = min(scores.shape[1], dim)
    
    if dim == 3 and scores.shape[1] >= 3:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        if labels is not None:
            unique_labels = np.unique(labels)
            colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))
            for i, lab in enumerate(unique_labels):
                mask = np.array(labels) == lab
                ax.scatter(scores.iloc[mask, 0], scores.iloc[mask, 1], scores.iloc[mask, 2],
                          c=[colors[i]], label=str(lab), s=40)
            ax.legend()
        else:
            ax.scatter(scores.iloc[:, 0], scores.iloc[:, 1], scores.iloc[:, 2],
                      c='steelblue', s=40, alpha=0.7)
        
        ax.set_xlabel(f"PC1 ({pca_result['explained_ratio'][0]:.1%})")
        ax.set_ylabel(f"PC2 ({pca_result['explained_ratio'][1]:.1%})")
        ax.set_zlabel(f"PC3 ({pca_result['explained_ratio'][2]:.1%})")
        ax.set_title("主成分3D散点图")
        
    else:
        fig, ax = plt.subplots(figsize=(10, 7))
        
        if labels is not None:
            unique_labels = np.unique(labels)
            colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))
            for i, lab in enumerate(unique_labels):
                mask = np.array(labels) == lab
                ax.scatter(scores.iloc[mask, 0], scores.iloc[mask, 1],
                          c=[colors[i]], label=str(lab), s=50, edgecolors='gray', linewidth=0.5)
            ax.legend()
        else:
            ax.scatter(scores.iloc[:, 0], scores.iloc[:, 1],
                      c='steelblue', s=50, alpha=0.7, edgecolors='gray', linewidth=0.5)
        
        ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
        ax.axvline(0, color='gray', linestyle='--', linewidth=0.5)
        ax.set_xlabel(f"PC1 ({pca_result['explained_ratio'][0]:.1%})")
        ax.set_ylabel(f"PC2 ({pca_result['explained_ratio'][1]:.1%})")
        ax.set_title("主成分2D散点图")
        ax.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig


def consistency_evaluation(df, threshold=0.9):
    """
    一致性评价（成对变量相关系数检验）。
    
    将df的列两两配对，计算Pearson相关系数平方，与阈值比较判定是否一致。
    
    Parameters
    ----------
    df : pd.DataFrame
        列为待评价的变量
    threshold : float
        一致性阈值（默认0.9）
    
    Returns
    -------
    pd.DataFrame
        每对变量的相关系数平方和判定结果
    """
    results = []
    cols = df.columns
    
    for i in range(0, len(cols) - 1, 2):
        if i + 1 < len(cols):
            r2 = df[cols[i]].corr(df[cols[i + 1]]) ** 2
            results.append({
                "变量1": cols[i],
                "变量2": cols[i + 1],
                "R²": r2,
                "判定": "一致" if r2 >= threshold else "不一致"
            })
    
    return pd.DataFrame(results)
