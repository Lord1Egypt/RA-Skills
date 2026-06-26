# IEEEtran 论文模板

## 基础文档类

```latex
\documentclass[conference]{IEEEtran}

% 中文支持（可选）
\usepackage{ctex}

% 基础包
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{IEEEtrantools}

% 参考文献样式
\bibliographystyle{IEEEtran}

% 标题信息
\title{论文标题（简洁有力，不超过15词）}

% 作者（多人用 \and 分隔）
\author{
  \IEEEauthorblockN{作者姓名}
  \IEEEauthorblockA{机构名称\\邮箱@example.com}
}

\begin{document}

% 摘要
\maketitle

\begin{abstract}
论文摘要，150-250词。简明扼要地描述：问题是什么、现有方法的不足、本文的解决方案、主要创新点、实验效果。不要缩写全文。
\end{abstract}

% 关键词
\begin{IEEEkeywords}
keyword1, keyword2, keyword3
\end{IEEEkeywords}

% 正文（双栏会自动排版）
\section{Introduction}
\section{Related Work}
\section{Proposed Method}
\section{Experiments}
\section{Conclusion}

% 参考文献
\bibliography{references}

\end{document}
```

## 常用格式命令

### 公式环境

```latex
% 单行公式（不编号）
\begin{equation*}
  f(x) = \sum_{i=1}^{n} w_i x_i + b
\end{equation*}

% 多行公式（编号）
\begin{align}
  \mathcal{L} &= \mathcal{L}_{\text{CE}} + \lambda \mathcal{L}_{\text{reg}} \\
  &= -\sum_{i} y_i \log \hat{y}_i + \lambda \|\theta\|^2
\end{align}
```

### 表格

```latex
\begin{table}[htbp]
  \caption{实验结果对比}
  \centering
  \begin{tabular}{lccc}
    \hline
    Method & Accuracy & F1 & Params \\
    \hline
    Baseline & 85.2\% & 0.84 & 1.2M \\
    Ours & 89.7\% & 0.89 & 1.5M \\
    \hline
  \end{tabular}
\end{table}
```

### 图片

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\linewidth]{figure1.png}
  \caption{模型框架图}
  \label{fig:framework}
\end{figure}
```

### 交叉引用

```latex
% 需要多次编译才能解析
如图~\ref{fig:framework}所示
公式~\eqref{eq:loss}表明
```

### 算法伪代码

```latex
\begin{algorithm}[htbp]
  \caption{算法名称}
  \label{alg:main}
  \begin{algorithmic}[1]
    \STATE Input: $X, Y$
    \STATE Initialize: $\theta$
    \FOR{each epoch}
      \STATE $\theta \gets \theta - \alpha \nabla \mathcal{L}$
    \ENDFOR
    \STATE Return $\theta$
  \end{algorithmic}
\end{algorithm}
```

## 注意事项

1. **图表位置**：`[htbp]` 允许浮动，不要强制位置
2. **引用标签**：`\label{fig:xxx}` 放在图表标题后
3. **参考文献格式**：
  ```latex
  \bibitem{key} 作者, ``标题,'' 会议/期刊, 年份.
  ```
