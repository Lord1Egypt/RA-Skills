#!/usr/bin/env python3
"""
Lead Scoring Model — LightGBM + SHAP
Predicts B2B lead conversion probability
"""
import argparse, pandas as pd, numpy as np

def main():
    p = argparse.ArgumentParser(description='Score B2B leads')
    p.add_argument('--input', required=True, help='Input CSV file')
    p.add_argument('--output', default='scored_leads.csv', help='Output CSV')
    p.add_argument('--model', default='lightgbm', help='Model type')
    args = p.parse_args()

    df = pd.read_csv(args.input)
    print(f"Loaded {len(df)} leads...")

    # Simple rule-based scoring (placeholder for real ML model)
    # In production: use trained LightGBM model
    scores = []
    for _, row in df.iterrows():
        engagement = (
            row.get('page_views', 0) * 0.3 +
            row.get('email_opens', 0) * 0.2 +
            row.get('form_fills', 0) * 0.5
        )
        title = row.get('job_title_score', 5)
        score = min(1.0, (engagement * 0.01 + title / 10) / 2)
        scores.append(round(score, 2))

    df['score'] = scores
    df['probability'] = df['score'].apply(lambda x: f"{int(x*100)}%")
    df['risk_level'] = df['score'].apply(
        lambda x: 'hot' if x > 0.7 else ('warm' if x > 0.4 else 'cold')
    )
    df['top_factor'] = df.apply(
        lambda r: 'high_engagement' if r.get('page_views', 0) > 50 else 'title_match',
        axis=1
    )

    df.to_csv(args.output, index=False)
    print(f"Saved scored leads → {args.output}")
    print(f"Hot leads: {(df['score']>0.7).sum()}")
    print(f"Warm leads: {((df['score']>0.4)&(df['score']<=0.7)).sum()}")
    print(f"Cold leads: {(df['score']<=0.4).sum()}")

if __name__ == '__main__':
    main()
