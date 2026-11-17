🏆 Competitive Data Science
Complete Reference Guide from Baseline to Topline


📖 Overview
Competitive Data Science is a comprehensive skill reference guide designed to systematically elevate your data science competition solutions from a basic Baseline to a competitive Topline.

This skill distills proven strategies and battle-tested techniques from real-world competitions including Kaggle, CCF BDCI, DCIC, and Tianchi. Each technique is accompanied by concrete Python code examples and practical implementation notes.

Whether you're a beginner aiming for your first medal or an experienced competitor looking to fill gaps in your workflow, this reference guide has you covered.

🎯 What This Skill Covers
Area	Key Topics
Data Processing	Cleaning, feature engineering, augmentation
Model Building	Traditional ML (LightGBM, XGBoost), Deep Learning (Transformer, FC), Adversarial Training
Training Techniques	Cross-validation, learning rate scheduling, gradient accumulation, mixed precision, EMA
Model Fusion	Rank fusion, stacking, K-fold ensemble, MC Dropout
Engineering Practices	Code organization, reproducibility, result naming, feature importance analysis
Competition Strategies	Single model optimization, multi-model fusion, data splitting, post-processing
📂 Repository Structure
text
competitive-data-science/
├── SKILL.md                  # Main skill document (431 lines)
├── example.py                # Sample code file
├── README.md                 # This file

🚀 Quick Start
1. Clone the Repository

```bash
git clone https://github.com/your-username/competitive-data-science.git
cd competitive-data-science
```

2. Read the Main Skill Document
```bash
cat SKILL.md
Or open it in your preferred editor to explore the complete reference guide.
```

3. Run Example Code
```bash
python example.py
4. Integrate into Your Workflow
Use the skill as a reference when working on your competition projects:
```
```python
# Import utility functions or reference patterns from example.py
from example import create_cv_folds, train_lgbm_model, ensemble_predictions
```
# Apply to your own competition
🔄 Core Workflow
The skill follows a systematic progression from baseline to topline:

text
┌─────────────────────────────────────────────────────────────────────┐
│                    COMPETITIVE DATA SCIENCE WORKFLOW               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│  │   BASELINE   │───▶│   IMPROVE    │───▶│   TOPLINE    │         │
│  └──────────────┘    └──────────────┘    └──────────────┘         │
│        │                    │                    │                  │
│        ▼                    ▼                    ▼                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│  │ Simple CV    │    │ EDA & FE     │    │ Ensemble     │         │
│  │ Simple model │    │ Tuning       │    │ Post-process │         │
│  │ First submit │    │ Multi-model  │    │ Final submit │         │
│  └──────────────┘    └──────────────┘    └──────────────┘         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
📊 Key Techniques Summary
Feature Engineering Checklist
Category	Techniques
Cleaning	Missing value imputation, outlier detection, data type correction
Creation	Cross-features (add/sub/mul/div), aggregations (groupby stats), polynomial features
Encoding	Label encoding, target encoding, frequency encoding, one-hot encoding
Selection	Feature importance ranking, recursive elimination, SHAP values
Augmentation	Pseudo-labeling, synthetic data generation, mixup
Model Selection Guide
Scenario	Recommended Models
Tabular data, < 1M rows	LightGBM, XGBoost, CatBoost
Tabular data, > 1M rows	LightGBM (with subsampling), XGBoost (hist)
Images	ResNet, EfficientNet, Vision Transformer
Text/NLP	BERT, RoBERTa, Transformer-based models
Time Series	LSTM, Transformer, TCN
Multi-modal	Hybrid: CNN + Transformer + Tabular models
Common Mistakes to Avoid
Mistake	Correct Approach
Overfitting to public LB	Use robust CV that correlates with LB
Data leakage	Split training/validation by time or group ID
Ignoring feature importance	Analyze and prune low-importance features
Using too complex model too early	Start simple, add complexity systematically
Not saving intermediate results	Version everything: code, features, predictions
🛠️ Example Code Snippets
Custom Cross-Validation Splitter
```python
from sklearn.model_selection import StratifiedKFold, GroupKFold

def create_cv_folds(df, target_col, group_col=None, n_folds=5):
    """
    Create cross-validation folds with optional grouping.
    """
    if group_col:
        gkf = GroupKFold(n_splits=n_folds)
        folds = gkf.split(df, df[target_col], groups=df[group_col])
    else:
        skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
        folds = skf.split(df, df[target_col])
    
    for fold_id, (train_idx, val_idx) in enumerate(folds):
        df.loc[val_idx, 'fold'] = fold_id
    
    return df
```
LightGBM Training with Optuna Tuning
```python
import optuna
import lightgbm as lgb

def objective(trial, X_train, y_train, X_val, y_val):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 500, 3000),
        'learning_rate': trial.suggest_loguniform('learning_rate', 0.01, 0.1),
        'num_leaves': trial.suggest_int('num_leaves', 31, 255),
        'max_depth': trial.suggest_int('max_depth', 3, 12),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 50),
        'subsample': trial.suggest_uniform('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_uniform('colsample_bytree', 0.5, 1.0),
        'reg_alpha': trial.suggest_loguniform('reg_alpha', 1e-8, 10.0),
        'reg_lambda': trial.suggest_loguniform('reg_lambda', 1e-8, 10.0),
    }
    
    model = lgb.LGBMClassifier(**params, random_state=42)
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)])
    return model.best_score_['valid_0']['binary_logloss']
```
Ensemble with Stacking
```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression

def create_stacking_ensemble(base_models, meta_model=None):
    """
    Create a stacking ensemble from base models.
    """
    if meta_model is None:
        meta_model = LogisticRegression()
    
    ensemble = StackingClassifier(
        estimators=[(f'model_{i}', model) for i, model in enumerate(base_models)],
        final_estimator=meta_model,
        cv=5,
        stack_method='predict_proba'
    )
    
    return ensemble
```
📁 SKILL.md Structure
The main SKILL.md document contains:

text
┌─────────────────────────────────────────────┐
│ Frontmatter                                 │
│  ├── name: competitive-data-science         │
│  └── description: Use when...               │
├─────────────────────────────────────────────┤
│ Overview                                    │
│  └── Core principles of systematic progress │
├─────────────────────────────────────────────┤
│ Core Workflow                               │
│  └── DOT format workflow diagram            │
├─────────────────────────────────────────────┤
│ Data Processing                             │
│  ├── Data cleaning                          │
│  ├── Feature engineering                    │
│  └── Data augmentation                      │
├─────────────────────────────────────────────┤
│ Model Building                              │
│  ├── Traditional ML                         │
│  ├── Deep Learning                          │
│  └── Adversarial Training                   │
├─────────────────────────────────────────────┤
│ Training Techniques                         │
│  ├── Cross-validation                       │
│  ├── Learning rate scheduling               │
│  ├── Gradient accumulation                  │
│  ├── Mixed precision                        │
│  └── EMA                                    │
├─────────────────────────────────────────────┤
│ Model Fusion                                │
│  ├── Rank fusion                            │
│  ├── Stacking                               │
│  ├── K-fold ensemble                        │
│  └── MC Dropout                             │
├─────────────────────────────────────────────┤
│ Engineering Practices                       │
│  ├── Code organization                      │
│  ├── Reproducibility                        │
│  ├── Result naming                          │
│  └── Feature importance analysis            │
├─────────────────────────────────────────────┤
│ Competition Strategies                      │
│  ├── Single model optimization              │
│  ├── Multi-model fusion                     │
│  ├── Data splitting                         │
│  └── Post-processing                        │
├─────────────────────────────────────────────┤
│ Quick Reference                             │
│  ├── Feature engineering checklist          │
│  ├── Model selection guide                  │
│  └── Common mistakes                        │
└─────────────────────────────────────────────┘
🤝 Contributing
Contributions are welcome! If you have:

Additional competition techniques to share

Code improvements or bug fixes

New example snippets

Documentation enhancements

Please see CONTRIBUTING.md for guidelines.

📚 References & Further Reading
Kaggle Competitions

CCF BDCI (Chinese)

DCIC (Chinese)

Approaching (Almost) Any ML Problem - Abhishek Thakur

Kaggle Solutions Collection

📄 License
This project is licensed under the MIT License — see the LICENSE file for details.

⭐ Star Us!
If you find this skill useful for your data science competitions, please consider giving it a ⭐ on GitHub!

🙏 Acknowledgments
The global data science competition community

Kaggle Grandmasters who openly share their knowledge

All contributors and users of this reference guide

Happy Competing! 🏆🚀
