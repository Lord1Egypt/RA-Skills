#!/usr/bin/env python3
"""AdvancedMLClassificationSkill

轻量化 AI 分类预测平台核心技能：
1. 读取 CSV 并执行标准化预处理。
2. 按算法生成训练代码（优先 Codex，失败时回退本地模板）。
3. 自动执行代码并计算准确率。
4. 可选执行交叉验证与参数搜索。
5. 生成新手友好的中文解读与可视化数据。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import textwrap
import traceback
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score
from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    RandomizedSearchCV,
    RepeatedStratifiedKFold,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler


@dataclass
class AlgorithmExecutionResult:
    """单个算法执行结果。"""

    accuracy: Optional[float]
    error: Optional[str]
    code: str
    cv_score: Optional[float] = None
    search_best_score: Optional[float] = None
    search_best_params: Optional[Dict[str, Any]] = None


class AdvancedMLClassificationSkill:
    """可复用的工业级分类算法对比技能。"""

    DEFAULT_ALGORITHMS = ["逻辑回归", "决策树", "随机森林", "XGBoost", "LightGBM"]

    ALGORITHM_ALIASES = {
        "逻辑回归": "逻辑回归",
        "logistic": "逻辑回归",
        "logisticregression": "逻辑回归",
        "决策树": "决策树",
        "decisiontree": "决策树",
        "tree": "决策树",
        "随机森林": "随机森林",
        "randomforest": "随机森林",
        "forest": "随机森林",
        "xgboost": "XGBoost",
        "xgb": "XGBoost",
        "lightgbm": "LightGBM",
        "lgbm": "LightGBM",
    }

    def __init__(
        self,
        data_path: str,
        target_col: str,
        algorithms: Optional[List[str]] = None,
        test_size: float = 0.2,
        random_state: int = 42,
        openai_api_key: Optional[str] = None,
        cv_options: Optional[Dict[str, Any]] = None,
        search_options: Optional[Dict[str, Any]] = None,
        feature_importance_enabled: bool = True,
    ) -> None:
        """初始化技能参数。"""
        self.data_path = data_path
        self.target_col = target_col
        self.algorithms = self._normalize_algorithms(algorithms or self.DEFAULT_ALGORITHMS)
        self.test_size = test_size
        self.random_state = random_state
        self.feature_importance_enabled = feature_importance_enabled

        self.generated_codes: Dict[str, str] = {}
        self.execution_errors: Dict[str, str] = {}

        if not 0 < self.test_size < 1:
            raise ValueError("test_size 必须在 (0, 1) 之间。")

        cv_options = cv_options or {}
        self.cv_options = {
            "enabled": bool(cv_options.get("enabled", False)),
            "method": str(cv_options.get("method", "StratifiedKFold")),
            "folds": int(cv_options.get("folds", 5)),
            "repeats": int(cv_options.get("repeats", 2)),
            "scoring": str(cv_options.get("scoring", "accuracy")),
        }

        search_options = search_options or {}
        self.search_options = {
            "enabled": bool(search_options.get("enabled", False)),
            "method": str(search_options.get("method", "GridSearchCV")),
            "cv": int(search_options.get("cv", 3)),
            "n_iter": int(search_options.get("n_iter", 20)),
            "scoring": str(search_options.get("scoring", "accuracy")),
        }

        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.openai_client = self._init_openai_client()

    def _init_openai_client(self) -> Any:
        """初始化 OpenAI 客户端（可选）。"""
        if not self.openai_api_key:
            return None

        try:
            from openai import OpenAI

            return OpenAI(api_key=self.openai_api_key)
        except Exception:
            return None

    def _normalize_algorithms(self, algorithms: List[str]) -> List[str]:
        """统一算法名称，支持中英文别名。"""
        normalized: List[str] = []
        for name in algorithms:
            key = str(name).strip().lower()
            canonical = self.ALGORITHM_ALIASES.get(key)
            if canonical is None:
                canonical = str(name).strip()
            if canonical and canonical not in normalized:
                normalized.append(canonical)
        return normalized

    @staticmethod
    def _merge_error(base_error: Optional[str], extra_error: Optional[str]) -> Optional[str]:
        """合并错误信息。"""
        if not base_error:
            return extra_error
        if not extra_error:
            return base_error
        return f"{base_error}\n{extra_error}"

    def _build_preprocessor(self, x_raw: pd.DataFrame) -> ColumnTransformer:
        """根据输入特征自动构建预处理器。"""
        numeric_features = x_raw.select_dtypes(include=["number", "bool"]).columns.tolist()
        categorical_features = [col for col in x_raw.columns if col not in numeric_features]

        transformers = []
        if numeric_features:
            transformers.append(
                (
                    "numeric",
                    Pipeline(
                        steps=[
                            ("imputer", SimpleImputer(strategy="median")),
                            ("scaler", StandardScaler()),
                        ]
                    ),
                    numeric_features,
                )
            )

        if categorical_features:
            transformers.append(
                (
                    "categorical",
                    Pipeline(
                        steps=[
                            ("imputer", SimpleImputer(strategy="most_frequent")),
                            (
                                "encoder",
                                OneHotEncoder(handle_unknown="ignore", sparse_output=True),
                            ),
                        ]
                    ),
                    categorical_features,
                )
            )

        if not transformers:
            raise ValueError("未检测到可用特征列。")

        return ColumnTransformer(transformers=transformers)

    def preprocess_data(self) -> Dict[str, Any]:
        """执行数据预处理。"""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"数据路径不存在: {self.data_path}")

        df = pd.read_csv(self.data_path)
        if self.target_col not in df.columns:
            raise KeyError(f"目标列不存在: {self.target_col}")

        df = df.dropna(subset=[self.target_col]).copy()
        if df.empty:
            raise ValueError("目标列全部为空，无法训练分类模型。")

        y_raw = df[self.target_col]
        x_raw = df.drop(columns=[self.target_col])
        if x_raw.empty:
            raise ValueError("特征列为空，请检查数据集内容。")

        label_encoder = LabelEncoder()
        y = pd.Series(label_encoder.fit_transform(y_raw), name=self.target_col)
        if y.nunique() < 2:
            raise ValueError("分类任务至少需要 2 个类别。")

        stratify_target = y if y.value_counts().min() > 1 else None
        x_train_raw, x_test_raw, y_train, y_test = train_test_split(
            x_raw,
            y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=stratify_target,
        )

        preprocessor = self._build_preprocessor(x_train_raw)
        x_train_processed = preprocessor.fit_transform(x_train_raw)
        x_test_processed = preprocessor.transform(x_test_raw)

        return {
            "x_train_raw": x_train_raw,
            "x_test_raw": x_test_raw,
            "x_train_processed": x_train_processed,
            "x_test_processed": x_test_processed,
            "y_train": y_train,
            "y_test": y_test,
            "n_classes": int(y.nunique()),
            "class_names": [str(item) for item in label_encoder.classes_],
            "feature_count": int(x_train_processed.shape[1]),
            "original_feature_names": list(x_train_raw.columns),
        }

    def _build_code_prompt(self, algorithm_name: str) -> str:
        """构造 Codex 提示词，要求返回可执行训练函数。"""
        return textwrap.dedent(
            f"""
            You are writing Python code for a classification benchmark.
            Generate ONLY executable Python code (no markdown).
            Requirements:
            1) Define function: train_and_evaluate(X_train, X_test, y_train, y_test, random_state, n_classes)
            2) Use algorithm: {algorithm_name}
            3) Include practical baseline hyperparameters
            4) Support both binary and multiclass classification
            5) Return a float accuracy score
            6) Use sklearn.metrics.accuracy_score

            Keep the code self-contained with necessary imports.
            """
        ).strip()

    def _local_algorithm_template(self, algorithm_name: str) -> str:
        """本地算法模板，作为 Codex 失败时的回退代码。"""
        if algorithm_name == "逻辑回归":
            body = """
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train_and_evaluate(X_train, X_test, y_train, y_test, random_state, n_classes):
    model = LogisticRegression(
        C=1.0,
        max_iter=600,
        solver="lbfgs"
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return accuracy_score(y_test, preds)
"""
        elif algorithm_name == "决策树":
            body = """
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def train_and_evaluate(X_train, X_test, y_train, y_test, random_state, n_classes):
    model = DecisionTreeClassifier(
        max_depth=8,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=random_state
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return accuracy_score(y_test, preds)
"""
        elif algorithm_name == "随机森林":
            body = """
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_and_evaluate(X_train, X_test, y_train, y_test, random_state, n_classes):
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        n_jobs=-1,
        random_state=random_state
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return accuracy_score(y_test, preds)
"""
        elif algorithm_name == "XGBoost":
            body = """
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

def train_and_evaluate(X_train, X_test, y_train, y_test, random_state, n_classes):
    objective = "multi:softprob" if n_classes > 2 else "binary:logistic"
    eval_metric = "mlogloss" if n_classes > 2 else "logloss"

    model = XGBClassifier(
        max_depth=6,
        learning_rate=0.1,
        n_estimators=300,
        subsample=0.9,
        colsample_bytree=0.9,
        objective=objective,
        eval_metric=eval_metric,
        random_state=random_state,
        tree_method="hist",
        n_jobs=-1,
        verbosity=0
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return accuracy_score(y_test, preds)
"""
        elif algorithm_name == "LightGBM":
            body = """
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score

def train_and_evaluate(X_train, X_test, y_train, y_test, random_state, n_classes):
    objective = "multiclass" if n_classes > 2 else "binary"

    model = LGBMClassifier(
        max_depth=-1,
        learning_rate=0.05,
        n_estimators=300,
        num_leaves=31,
        subsample=0.9,
        colsample_bytree=0.9,
        objective=objective,
        random_state=random_state,
        verbose=-1
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return accuracy_score(y_test, preds)
"""
        else:
            raise ValueError(f"不支持的算法: {algorithm_name}")

        return textwrap.dedent(body).strip() + "\n"

    @staticmethod
    def _strip_code_fence(text: str) -> str:
        """移除模型可能返回的 Markdown 代码块。"""
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
        return cleaned.strip()

    def generate_algorithm_code(self, algorithm_name: str) -> str:
        """生成单个算法训练代码（Codex 优先，本地模板兜底）。"""
        fallback_code = self._local_algorithm_template(algorithm_name)

        if not self.openai_client:
            return fallback_code

        prompt = self._build_code_prompt(algorithm_name)
        try:
            response = self.openai_client.completions.create(
                model="code-davinci-002",
                prompt=prompt,
                max_tokens=900,
                temperature=0.2,
            )
            candidate = self._strip_code_fence(response.choices[0].text)
            if "def train_and_evaluate" not in candidate:
                return fallback_code
            return candidate + "\n"
        except Exception:
            return fallback_code

    @staticmethod
    def _dependency_hint(algorithm_name: str) -> Optional[str]:
        """检查算法依赖并返回安装提示。"""
        if algorithm_name == "XGBoost" and importlib.util.find_spec("xgboost") is None:
            return "缺少依赖 xgboost，请执行: pip install xgboost"
        if algorithm_name == "LightGBM" and importlib.util.find_spec("lightgbm") is None:
            return "缺少依赖 lightgbm，请执行: pip install lightgbm"
        return None

    @staticmethod
    def _runtime_lib_hint(exc: Exception) -> Optional[str]:
        """根据运行时异常补充依赖修复建议。"""
        lowered = str(exc).lower()
        if "libomp" in lowered:
            return "检测到缺少 OpenMP 运行时，请执行: brew install libomp"
        return None

    def _build_estimator(self, algorithm_name: str, n_classes: int) -> Any:
        """构建内置估计器，用于交叉验证/参数搜索/特征重要性。"""
        if algorithm_name == "逻辑回归":
            from sklearn.linear_model import LogisticRegression

            return LogisticRegression(C=1.0, max_iter=600, solver="lbfgs")

        if algorithm_name == "决策树":
            from sklearn.tree import DecisionTreeClassifier

            return DecisionTreeClassifier(
                max_depth=8,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=self.random_state,
            )

        if algorithm_name == "随机森林":
            from sklearn.ensemble import RandomForestClassifier

            return RandomForestClassifier(
                n_estimators=300,
                max_depth=12,
                min_samples_split=5,
                min_samples_leaf=2,
                n_jobs=-1,
                random_state=self.random_state,
            )

        if algorithm_name == "XGBoost":
            from xgboost import XGBClassifier

            objective = "multi:softprob" if n_classes > 2 else "binary:logistic"
            eval_metric = "mlogloss" if n_classes > 2 else "logloss"
            params = {
                "max_depth": 6,
                "learning_rate": 0.1,
                "n_estimators": 300,
                "subsample": 0.9,
                "colsample_bytree": 0.9,
                "objective": objective,
                "eval_metric": eval_metric,
                "random_state": self.random_state,
                "tree_method": "hist",
                "n_jobs": -1,
                "verbosity": 0,
            }
            if n_classes > 2:
                params["num_class"] = n_classes
            return XGBClassifier(**params)

        if algorithm_name == "LightGBM":
            from lightgbm import LGBMClassifier

            objective = "multiclass" if n_classes > 2 else "binary"
            params = {
                "max_depth": -1,
                "learning_rate": 0.05,
                "n_estimators": 300,
                "num_leaves": 31,
                "subsample": 0.9,
                "colsample_bytree": 0.9,
                "objective": objective,
                "random_state": self.random_state,
                "verbose": -1,
            }
            if n_classes > 2:
                params["num_class"] = n_classes
            return LGBMClassifier(**params)

        raise ValueError(f"不支持的算法: {algorithm_name}")

    def _build_training_pipeline(
        self,
        algorithm_name: str,
        n_classes: int,
        x_train_raw: pd.DataFrame,
    ) -> Pipeline:
        """构建预处理+模型的一体化流水线。"""
        preprocessor = self._build_preprocessor(x_train_raw)
        model = self._build_estimator(algorithm_name, n_classes)
        return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])

    def _build_cv_splitter(self, y_train: pd.Series) -> Any:
        """根据配置构建交叉验证切分器。"""
        method = self.cv_options["method"].strip().lower()
        folds = max(2, int(self.cv_options["folds"]))

        if method == "kfold":
            return KFold(n_splits=folds, shuffle=True, random_state=self.random_state)

        if method in {"repeatedstratifiedkfold", "repeated_stratified_kfold"}:
            repeats = max(1, int(self.cv_options["repeats"]))
            return RepeatedStratifiedKFold(
                n_splits=folds,
                n_repeats=repeats,
                random_state=self.random_state,
            )

        if y_train.value_counts().min() <= 1:
            return KFold(n_splits=folds, shuffle=True, random_state=self.random_state)

        return StratifiedKFold(n_splits=folds, shuffle=True, random_state=self.random_state)

    def _get_param_space(self, algorithm_name: str) -> Dict[str, List[Any]]:
        """定义参数搜索空间。"""
        if algorithm_name == "逻辑回归":
            return {
                "model__C": [0.1, 0.5, 1.0, 3.0, 10.0],
                "model__max_iter": [400, 700, 1000],
            }

        if algorithm_name == "决策树":
            return {
                "model__max_depth": [4, 8, 12, None],
                "model__min_samples_split": [2, 5, 10],
                "model__min_samples_leaf": [1, 2, 4],
            }

        if algorithm_name == "随机森林":
            return {
                "model__n_estimators": [200, 300, 500],
                "model__max_depth": [8, 12, None],
                "model__min_samples_split": [2, 5, 10],
                "model__min_samples_leaf": [1, 2, 4],
            }

        if algorithm_name == "XGBoost":
            return {
                "model__max_depth": [4, 6, 8],
                "model__learning_rate": [0.03, 0.05, 0.1],
                "model__n_estimators": [200, 300, 500],
                "model__subsample": [0.8, 0.9, 1.0],
                "model__colsample_bytree": [0.8, 0.9, 1.0],
            }

        if algorithm_name == "LightGBM":
            return {
                "model__num_leaves": [31, 63, 127],
                "model__learning_rate": [0.03, 0.05, 0.1],
                "model__n_estimators": [200, 300, 500],
                "model__subsample": [0.8, 0.9, 1.0],
                "model__colsample_bytree": [0.8, 0.9, 1.0],
            }

        raise ValueError(f"不支持的算法: {algorithm_name}")

    @staticmethod
    def _strip_model_prefix(params: Dict[str, Any]) -> Dict[str, Any]:
        """去除 Pipeline 参数前缀。"""
        cleaned: Dict[str, Any] = {}
        for key, value in params.items():
            cleaned[key.replace("model__", "")] = value
        return cleaned

    def _run_cross_validation(
        self,
        algorithm_name: str,
        data_bundle: Dict[str, Any],
    ) -> float:
        """运行交叉验证并返回均值准确率。"""
        pipeline = self._build_training_pipeline(
            algorithm_name=algorithm_name,
            n_classes=data_bundle["n_classes"],
            x_train_raw=data_bundle["x_train_raw"],
        )

        splitter = self._build_cv_splitter(data_bundle["y_train"])
        scores = cross_val_score(
            pipeline,
            data_bundle["x_train_raw"],
            data_bundle["y_train"],
            cv=splitter,
            scoring=self.cv_options["scoring"],
            n_jobs=1,
            error_score="raise",
        )
        return round(float(scores.mean()), 4)

    def _run_hyperparameter_search(
        self,
        algorithm_name: str,
        data_bundle: Dict[str, Any],
    ) -> Dict[str, Any]:
        """运行参数搜索并返回最优结果。"""
        pipeline = self._build_training_pipeline(
            algorithm_name=algorithm_name,
            n_classes=data_bundle["n_classes"],
            x_train_raw=data_bundle["x_train_raw"],
        )
        param_space = self._get_param_space(algorithm_name)

        method = self.search_options["method"].strip().lower()
        if method == "randomizedsearchcv":
            searcher = RandomizedSearchCV(
                estimator=pipeline,
                param_distributions=param_space,
                n_iter=max(1, int(self.search_options["n_iter"])),
                cv=max(2, int(self.search_options["cv"])),
                scoring=self.search_options["scoring"],
                random_state=self.random_state,
                n_jobs=1,
            )
        else:
            searcher = GridSearchCV(
                estimator=pipeline,
                param_grid=param_space,
                cv=max(2, int(self.search_options["cv"])),
                scoring=self.search_options["scoring"],
                n_jobs=1,
            )

        searcher.fit(data_bundle["x_train_raw"], data_bundle["y_train"])
        return {
            "best_score": round(float(searcher.best_score_), 4),
            "best_params": self._strip_model_prefix(searcher.best_params_),
        }

    def run_algorithm(
        self,
        algorithm_name: str,
        data_bundle: Dict[str, Any],
    ) -> AlgorithmExecutionResult:
        """执行算法代码并返回准确率与错误信息。"""
        dep_error = self._dependency_hint(algorithm_name)
        if dep_error:
            code = self._local_algorithm_template(algorithm_name)
            return AlgorithmExecutionResult(accuracy=None, error=dep_error, code=code)

        try:
            code = self.generate_algorithm_code(algorithm_name)
        except Exception as exc:
            code = self._local_algorithm_template(algorithm_name)
            return AlgorithmExecutionResult(
                accuracy=None,
                error=f"代码生成失败: {exc}",
                code=code,
            )

        error: Optional[str] = None
        accuracy: Optional[float] = None
        namespace: Dict[str, Any] = {}

        try:
            exec(code, namespace)  # noqa: S102
            train_fn = namespace.get("train_and_evaluate")
            if not callable(train_fn):
                raise ValueError("生成代码中未定义 train_and_evaluate 函数。")

            score = train_fn(
                data_bundle["x_train_processed"],
                data_bundle["x_test_processed"],
                data_bundle["y_train"],
                data_bundle["y_test"],
                self.random_state,
                data_bundle["n_classes"],
            )
            accuracy = round(float(score), 4)
        except Exception as exc:
            trace = traceback.format_exc(limit=2)
            hint = self._runtime_lib_hint(exc)
            error = f"执行失败: {exc}\n{trace}"
            if hint:
                error = f"{error}\n{hint}"

        cv_score: Optional[float] = None
        if self.cv_options["enabled"]:
            try:
                cv_score = self._run_cross_validation(algorithm_name, data_bundle)
            except Exception as exc:
                extra = f"交叉验证失败: {exc}"
                hint = self._runtime_lib_hint(exc)
                if hint:
                    extra = f"{extra}；{hint}"
                error = self._merge_error(error, extra)

        search_best_score: Optional[float] = None
        search_best_params: Optional[Dict[str, Any]] = None
        if self.search_options["enabled"]:
            try:
                search_result = self._run_hyperparameter_search(algorithm_name, data_bundle)
                search_best_score = search_result["best_score"]
                search_best_params = search_result["best_params"]
            except Exception as exc:
                extra = f"参数搜索失败: {exc}"
                hint = self._runtime_lib_hint(exc)
                if hint:
                    extra = f"{extra}；{hint}"
                error = self._merge_error(error, extra)

        return AlgorithmExecutionResult(
            accuracy=accuracy,
            error=error,
            code=code,
            cv_score=cv_score,
            search_best_score=search_best_score,
            search_best_params=search_best_params,
        )

    def compute_feature_importance(
        self,
        algorithm_name: str,
        data_bundle: Dict[str, Any],
        best_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """对最佳算法计算置换特征重要性。"""
        pipeline = self._build_training_pipeline(
            algorithm_name=algorithm_name,
            n_classes=data_bundle["n_classes"],
            x_train_raw=data_bundle["x_train_raw"],
        )

        if best_params:
            pipeline.named_steps["model"].set_params(**best_params)

        pipeline.fit(data_bundle["x_train_raw"], data_bundle["y_train"])
        perm = permutation_importance(
            pipeline,
            data_bundle["x_test_raw"],
            data_bundle["y_test"],
            scoring="accuracy",
            n_repeats=8,
            random_state=self.random_state,
            n_jobs=1,
        )

        names = data_bundle["original_feature_names"]
        items = []
        for idx, feature_name in enumerate(names):
            items.append(
                {
                    "feature": str(feature_name),
                    "importance": round(float(perm.importances_mean[idx]), 6),
                    "std": round(float(perm.importances_std[idx]), 6),
                }
            )

        items.sort(key=lambda row: row["importance"], reverse=True)
        return {
            "algorithm": algorithm_name,
            "scoring": "accuracy",
            "items": items,
        }

    def _local_interpretation(
        self,
        accuracy_results: Dict[str, Optional[float]],
        errors: Dict[str, str],
        cv_results: Dict[str, Optional[float]],
        search_results: Dict[str, Dict[str, Any]],
    ) -> str:
        """本地规则生成中文解读。"""
        valid_scores = {k: v for k, v in accuracy_results.items() if isinstance(v, float)}
        if not valid_scores:
            message = "所有算法都未成功执行，请优先检查数据质量与依赖安装。"
            if errors:
                message += " 典型错误: " + "；".join(f"{k}: {v.splitlines()[0]}" for k, v in errors.items())
            return message

        ranked = sorted(valid_scores.items(), key=lambda item: item[1], reverse=True)
        best_name, best_score = ranked[0]

        traditional = [name for name in ["逻辑回归", "决策树", "随机森林"] if name in valid_scores]
        industrial = [name for name in ["XGBoost", "LightGBM"] if name in valid_scores]

        lines = [
            f"本次测试中表现最好的算法是 {best_name}，测试集准确率为 {best_score:.4f}。",
            "传统算法通常训练速度更快、解释性更强；工业级算法在复杂特征下通常有更高上限。",
        ]

        if traditional:
            trad_best = max(traditional, key=lambda name: valid_scores[name])
            lines.append(f"传统算法里最佳为 {trad_best}（{valid_scores[trad_best]:.4f}）。")

        if industrial:
            ind_best = max(industrial, key=lambda name: valid_scores[name])
            lines.append(f"工业级算法里最佳为 {ind_best}（{valid_scores[ind_best]:.4f}）。")

        if self.cv_options["enabled"]:
            cv_valid = {k: v for k, v in cv_results.items() if isinstance(v, float)}
            if cv_valid:
                cv_best = max(cv_valid, key=cv_valid.get)
                lines.append(
                    f"在 {self.cv_options['method']} 下，交叉验证平均分最高的是 {cv_best}（{cv_valid[cv_best]:.4f}）。"
                )

        if self.search_options["enabled"] and search_results:
            search_scores = {
                name: info["best_score"]
                for name, info in search_results.items()
                if isinstance(info.get("best_score"), float)
            }
            if search_scores:
                search_best = max(search_scores, key=search_scores.get)
                lines.append(
                    f"参数搜索后最优算法是 {search_best}，最佳交叉验证分数 {search_scores[search_best]:.4f}。"
                )

        if errors:
            lines.append(
                "以下算法存在报错，请按提示修复后重试："
                + "；".join(f"{name}: {msg.splitlines()[0]}" for name, msg in errors.items())
            )

        lines.append("建议下一步将最佳模型做业务阈值分析，并结合特征重要性制定优化策略。")
        return "\n".join(lines)

    def interpret_results(
        self,
        accuracy_results: Dict[str, Optional[float]],
        errors: Dict[str, str],
        cv_results: Dict[str, Optional[float]],
        search_results: Dict[str, Dict[str, Any]],
    ) -> str:
        """调用 GPT-3.5 生成中文解读，失败时回退本地规则。"""
        fallback = self._local_interpretation(
            accuracy_results=accuracy_results,
            errors=errors,
            cv_results=cv_results,
            search_results=search_results,
        )

        if not self.openai_client:
            return fallback

        prompt_payload = {
            "accuracy_results": accuracy_results,
            "cv_results": cv_results,
            "search_results": search_results,
            "errors": errors,
            "task": "请面向初级数据开发师，用中文解读分类结果，重点比较传统算法与工业级算法差异。",
        }

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.2,
                messages=[
                    {
                        "role": "system",
                        "content": "你是机器学习讲师，请输出结构清晰、简洁可执行的中文结果解读。",
                    },
                    {"role": "user", "content": json.dumps(prompt_payload, ensure_ascii=False)},
                ],
            )
            text = response.choices[0].message.content.strip()
            return text or fallback
        except Exception:
            return fallback

    def get_visualization_data(
        self,
        accuracy_results: Dict[str, Optional[float]],
        cv_results: Dict[str, Optional[float]],
    ) -> Dict[str, Any]:
        """生成前端图表数据。"""
        algorithms: List[str] = []
        accuracies: List[float] = []
        cv_scores: List[Optional[float]] = []

        for name, score in accuracy_results.items():
            if isinstance(score, float):
                algorithms.append(name)
                accuracies.append(round(score, 4))
                cv_value = cv_results.get(name)
                cv_scores.append(round(cv_value, 4) if isinstance(cv_value, float) else None)

        return {
            "algorithms": algorithms,
            "accuracies": accuracies,
            "cv_scores": cv_scores,
            "bar_series": {"x": algorithms, "y": accuracies, "name": "测试集准确率"},
            "line_series": {"x": algorithms, "y": accuracies, "name": "测试集准确率趋势"},
            "cv_line_series": {"x": algorithms, "y": cv_scores, "name": "交叉验证平均分"},
        }

    def run(self) -> Dict[str, Any]:
        """执行完整技能流程并返回结构化结果。"""
        data_bundle = self.preprocess_data()

        accuracy_results: Dict[str, Optional[float]] = {}
        generated_codes: Dict[str, str] = {}
        cv_results: Dict[str, Optional[float]] = {}
        search_results: Dict[str, Dict[str, Any]] = {}

        for algorithm_name in self.algorithms:
            if algorithm_name not in self.DEFAULT_ALGORITHMS:
                accuracy_results[algorithm_name] = None
                generated_codes[algorithm_name] = (
                    "# Unsupported algorithm\n"
                    "def train_and_evaluate(*args, **kwargs):\n"
                    "    raise ValueError('Unsupported algorithm')\n"
                )
                cv_results[algorithm_name] = None
                self.execution_errors[algorithm_name] = f"不支持的算法: {algorithm_name}"
                continue

            try:
                result = self.run_algorithm(
                    algorithm_name=algorithm_name,
                    data_bundle=data_bundle,
                )
                accuracy_results[algorithm_name] = result.accuracy
                generated_codes[algorithm_name] = result.code
                cv_results[algorithm_name] = result.cv_score

                if isinstance(result.search_best_score, float):
                    search_results[algorithm_name] = {
                        "best_score": result.search_best_score,
                        "best_params": result.search_best_params or {},
                    }

                if result.error:
                    self.execution_errors[algorithm_name] = result.error
            except Exception as exc:
                accuracy_results[algorithm_name] = None
                generated_codes[algorithm_name] = self._local_algorithm_template(algorithm_name)
                cv_results[algorithm_name] = None
                self.execution_errors[algorithm_name] = f"运行中断: {exc}"

        feature_importance: Dict[str, Any] = {}
        if self.feature_importance_enabled:
            valid_scores = {k: v for k, v in accuracy_results.items() if isinstance(v, float)}
            if valid_scores:
                best_algorithm = max(valid_scores, key=valid_scores.get)
                try:
                    best_params = search_results.get(best_algorithm, {}).get("best_params")
                    feature_importance = self.compute_feature_importance(
                        algorithm_name=best_algorithm,
                        data_bundle=data_bundle,
                        best_params=best_params,
                    )
                except Exception as exc:
                    self.execution_errors[best_algorithm] = self._merge_error(
                        self.execution_errors.get(best_algorithm),
                        f"特征重要性计算失败: {exc}",
                    ) or "特征重要性计算失败"

        interpretation = self.interpret_results(
            accuracy_results=accuracy_results,
            errors=self.execution_errors,
            cv_results=cv_results,
            search_results=search_results,
        )
        visualization_data = self.get_visualization_data(accuracy_results, cv_results)

        return {
            "accuracy_results": accuracy_results,
            "cv_results": cv_results,
            "search_results": search_results,
            "interpretation": interpretation,
            "generated_codes": generated_codes,
            "visualization_data": visualization_data,
            "feature_importance": feature_importance,
        }


def run_skill(params: Dict[str, Any]) -> Dict[str, Any]:
    """OpenClaw 风格的技能入口函数。"""
    skill = AdvancedMLClassificationSkill(
        data_path=params["data_path"],
        target_col=params["target_col"],
        algorithms=params.get("algorithms"),
        test_size=params.get("test_size", 0.2),
        random_state=params.get("random_state", 42),
        openai_api_key=params.get("openai_api_key"),
        cv_options=params.get("cv_options"),
        search_options=params.get("search_options"),
        feature_importance_enabled=params.get("feature_importance_enabled", True),
    )
    return skill.run()


def parse_args() -> argparse.Namespace:
    """命令行参数。"""
    parser = argparse.ArgumentParser(description="Advanced ML Classification Skill")
    parser.add_argument("--data-path", required=True, help="CSV 数据路径")
    parser.add_argument("--target-col", required=True, help="目标列名")
    parser.add_argument(
        "--algorithms",
        default=",".join(AdvancedMLClassificationSkill.DEFAULT_ALGORITHMS),
        help="算法列表，逗号分隔",
    )
    parser.add_argument("--test-size", type=float, default=0.2, help="测试集比例")
    parser.add_argument("--random-state", type=int, default=42, help="随机种子")

    parser.add_argument("--enable-cv", action="store_true", help="开启交叉验证")
    parser.add_argument(
        "--cv-method",
        default="StratifiedKFold",
        choices=["StratifiedKFold", "KFold", "RepeatedStratifiedKFold"],
        help="交叉验证方式",
    )
    parser.add_argument("--cv-folds", type=int, default=5, help="交叉验证折数")
    parser.add_argument("--cv-repeats", type=int, default=2, help="重复交叉验证重复次数")
    parser.add_argument("--cv-scoring", default="accuracy", help="交叉验证评分指标")

    parser.add_argument("--enable-search", action="store_true", help="开启参数搜索")
    parser.add_argument(
        "--search-method",
        default="GridSearchCV",
        choices=["GridSearchCV", "RandomizedSearchCV"],
        help="参数搜索方式",
    )
    parser.add_argument("--search-cv", type=int, default=3, help="参数搜索交叉验证折数")
    parser.add_argument("--search-n-iter", type=int, default=20, help="随机搜索迭代次数")
    parser.add_argument("--search-scoring", default="accuracy", help="参数搜索评分指标")

    parser.add_argument(
        "--disable-feature-importance",
        action="store_true",
        help="关闭特征重要性计算",
    )
    return parser.parse_args()


def main() -> None:
    """CLI 示例入口。"""
    args = parse_args()
    algorithms = [item.strip() for item in args.algorithms.split(",") if item.strip()]

    result = run_skill(
        {
            "data_path": args.data_path,
            "target_col": args.target_col,
            "algorithms": algorithms,
            "test_size": args.test_size,
            "random_state": args.random_state,
            "cv_options": {
                "enabled": args.enable_cv,
                "method": args.cv_method,
                "folds": args.cv_folds,
                "repeats": args.cv_repeats,
                "scoring": args.cv_scoring,
            },
            "search_options": {
                "enabled": args.enable_search,
                "method": args.search_method,
                "cv": args.search_cv,
                "n_iter": args.search_n_iter,
                "scoring": args.search_scoring,
            },
            "feature_importance_enabled": not args.disable_feature_importance,
        }
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
