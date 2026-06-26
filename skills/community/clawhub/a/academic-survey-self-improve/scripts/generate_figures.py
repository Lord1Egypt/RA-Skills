#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate TikZ figures for academic surveys
"""

def generate_taxonomy_figure():
    """Generate taxonomy tree diagram"""
    return r"""
\begin{figure}[t]
    \centering
    \begin{tikzpicture}[
        level distance=1.5cm,
        level 1/.style={sibling distance=3cm},
        level 2/.style={sibling distance=2cm},
        box/.style={rectangle, draw, rounded corners, align=center, minimum width=2cm, minimum height=0.8cm, fill=blue!10},
        arrow/.style={->, >=stealth, thick}
    ]
    \node[box] {MoE Approaches}
        child {node[box] {Routing\\Strategy}
            child {node[box] {Top-K}}
            child {node[box] {Expert\\Choice}}
        }
        child {node[box] {Expert\\Granularity}
            child {node[box] {Fine}}
            child {node[box] {Coarse}}
        }
        child {node[box] {Parallelism}
            child {node[box] {Data}}
            child {node[box] {Expert}}
        };
    \end{tikzpicture}
    \caption{Taxonomy of MoE approaches across three dimensions.}
    \label{fig:taxonomy}
\end{figure}
"""

def generate_architecture_figure():
    """Generate model architecture diagram"""
    return r"""
\begin{figure}[t]
    \centering
    \begin{tikzpicture}[
        node distance=1cm,
        block/.style={rectangle, draw, minimum width=3cm, minimum height=1cm, align=center},
        arrow/.style={->, >=stealth, thick}
    ]
    \node[block, fill=blue!20] (input) {Input};
    \node[block, below=of input, fill=green!20] (embedding) {Token Embedding};
    \node[block, below=of embedding, fill=yellow!20] (transformer) {Transformer Layers\\(N=61)};
    \node[block, below=of transformer, split rectangle, fill=orange!20] (moe) {MoE Layer\\256 Experts};
    \node[block, below=of moe, fill=red!20] (output) {Output};
    
    \draw[arrow] (input) -- (embedding);
    \draw[arrow] (embedding) -- (transformer);
    \draw[arrow] (transformer) -- (moe);
    \draw[arrow] (moe) -- (output);
    \end{tikzpicture}
    \caption{Model architecture overview.}
    \label{fig:architecture}
\end{figure}
"""

def generate_comparison_chart():
    """Generate performance comparison chart"""
    return r"""
\begin{figure}[t]
    \centering
    \begin{tikzpicture}
    \begin{axis}[
        ybar,
        bar width=15pt,
        width=\columnwidth,
        height=6cm,
        enlargelimits=0.15,
        legend style={at={(0.5,-0.15)}, anchor=north,legend columns=-1},
        ylabel={Score},
        symbolic x coords={MMLU, GSM8K, HumanEval, MATH},
        xtick=data,
        nodes near coords,
        nodes near coords align={vertical},
    ]
    \addplot coordinates {(MMLU, 88.5) (GSM8K, 92.3) (HumanEval, 85.6) (MATH, 78.9)};
    \addplot coordinates {(MMLU, 86.4) (GSM8K, 92.0) (HumanEval, 87.2) (MATH, 76.5)};
    \addplot coordinates {(MMLU, 79.3) (GSM8K, 84.2) (HumanEval, 72.1) (MATH, 62.4)};
    \legend{Model A, Model B, Model C}
    \end{axis}
    \end{tikzpicture}
    \caption{Performance comparison across benchmarks.}
    \label{fig:comparison}
\end{figure}
"""

def generate_timeline_figure():
    """Generate research timeline"""
    return r"""
\begin{figure}[t]
    \centering
    \begin{tikzpicture}[
        timeline/.style={line width=2pt, ->},
        event/.style={circle, draw, fill=white, inner sep=2pt},
        year/.style={font=\small, text=gray}
    ]
    \draw[timeline] (0,0) -- (10,0);
    
    \node[event, fill=blue!20] at (1,0) {};
    \node[year, above=5pt] at (1,0) {2017};
    \node[below=5pt, align=center] at (1,0) {Transformer};
    
    \node[event, fill=green!20] at (3,0) {};
    \node[year, above=5pt] at (3,0) {2019};
    \node[below=5pt, align=center] at (3,0) {MoE};
    
    \node[event, fill=yellow!20] at (5,0) {};
    \node[year, above=5pt] at (5,0) {2021};
    \node[below=5pt, align=center] at (5,0) {Switch};
    
    \node[event, fill=orange!20] at (7,0) {};
    \node[year, above=5pt] at (7,0) {2023};
    \node[below=5pt, align=center] at (7,0) {Mixtral};
    
    \node[event, fill=red!20] at (9,0) {};
    \node[year, above=5pt] at (9,0) {2024};
    \node[below=5pt, align=center] at (9,0) {DeepSeek-V3};
    \end{tikzpicture}
    \caption{Timeline of key developments in MoE research.}
    \label{fig:timeline}
\end{figure}
"""

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_figures.py <output_dir>")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    
    figures = {
        'taxonomy': generate_taxonomy_figure(),
        'architecture': generate_architecture_figure(),
        'comparison': generate_comparison_chart(),
        'timeline': generate_timeline_figure()
    }
    
    for name, content in figures.items():
        with open(f'{output_dir}/figures/{name}.tex', 'w') as f:
            f.write(content)
        print(f"✓ Generated {name}.tex")
    
    print(f"\nGenerated {len(figures)} figures in {output_dir}/figures/")

if __name__ == '__main__':
    import os
    os.makedirs('output/figures', exist_ok=True)
    main()
