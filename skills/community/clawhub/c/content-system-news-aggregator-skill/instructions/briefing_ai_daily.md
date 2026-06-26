# 🧠 AI Deep Dive Instructions (AI 深度日报)

> **INPUT**: JSON object with `newsletter_picks`, `huggingface_papers` sections.
> **OUTPUT**: A deep-dive AI report focusing on research, industry analysis, and key tech updates.

---

## 🎯 Focus Areas
1.  **SOTA Research**: Deep analysis of top papers from Hugging Face. Focus on methodology and results.
2.  **Industry Analysis**: Strategic insights from top AI newsletters (ChinAI, Memia, etc.).

## ⚠️ Anti-Laziness Protocol
1.  **Volume**: Output MUST contain at least **15 items** across all sections.
2.  **Depth**: For papers and newsletters, provide **2-3 bullet points** of analysis (Why it matters, Key takeaway).

## 📝 Report Structure

### Part 1: 🔬 SOTA Research (Hugging Face Papers)
*   **Data Source**: Hugging Face Daily Papers
*   **Format**:
    ```markdown
    #### 1. [Title (Translated)](url)
    - **Source**: Hugging Face Papers | **Time**: Today
    - **Summary**: One sentence summary of the paper's contribution.
    - **Deep Dive**:
        *   **Innovation**: Key technical novelty (e.g., "New attention mechanism").
        *   **Impact**: Potential applications or performance gains.
    ```

### Part 2: 📧 Industry Insights (Newsletters)
*   **Data Source**: AI Newsletters (ChinAI, Memia, etc.)
*   **Focus**: Strategic shifts, policy changes, major product launches.
*   **Format**:
    ```markdown
    #### 1. [Title (Translated)](url)
    - **Source**: Newsletter Name | **Time**: X hours ago
    - **Summary**: Concise overview of the newsletter topic.
    - **Insight**: 💡 Strategic implication or key takeaway.
    ```


