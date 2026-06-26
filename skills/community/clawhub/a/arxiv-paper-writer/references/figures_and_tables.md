# Figures and Tables Reference

Use this reference when creating reproducible paper visuals.

## Principles

- Prefer TikZ and LaTeX tables when the figure is conceptual, architectural, or taxonomic.
- Use external image files only when the paper needs plots, screenshots, or complex visual assets.
- Every figure/table should support a specific claim in the text.
- Keep captions explanatory enough that readers understand the artifact without reading the full section.

## Recommended survey artifacts

For arXiv-style survey papers, create 2-5 high-value artifacts:

1. timeline figure
2. architecture diagram
3. taxonomy table
4. framework/system comparison table
5. benchmark or limitation matrix

## TikZ architecture pattern

```latex
\begin{figure}[t]
\centering
\begin{tikzpicture}[
  node distance=1.5cm,
  box/.style={rectangle,rounded corners,draw=black,thick,align=center,minimum width=2.5cm,minimum height=0.8cm},
  arrow/.style={-{Latex[length=3mm]},thick}
]
\node[box] (input) {Input};
\node[box,right=of input] (reason) {Reasoning};
\node[box,right=of reason] (action) {Action};
\draw[arrow] (input) -- (reason);
\draw[arrow] (reason) -- (action);
\end{tikzpicture}
\caption{A minimal architecture diagram.}
\label{fig:architecture}
\end{figure}
```

## Booktabs table pattern

```latex
\begin{table}[t]
\centering
\caption{Comparison of representative systems.}
\label{tab:systems}
\begin{tabularx}{\linewidth}{l l l X}
\toprule
System & Year & Type & Key idea \\
\midrule
System A & 2023 & Framework & Short description. \\
System B & 2024 & Benchmark & Short description. \\
\bottomrule
\end{tabularx}
\end{table}
```
