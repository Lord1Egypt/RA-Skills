# Intelligence package
from engine.intelligence.categoriser import categorise_records
from engine.intelligence.anomaly_detector import detect_anomalies
from engine.intelligence.recommender import generate_recommendations
from engine.intelligence.financial_model import FinancialModelManager

__all__ = [
    "categorise_records",
    "detect_anomalies",
    "generate_recommendations",
    "FinancialModelManager",
]
