import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from typing import Any, Dict, List, Tuple

from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("canslim_analysis.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

SCHEMA_VERSION = "2.1"


def default_ai_checks() -> Dict[str, Any]:
    return {
        "N_New_Catalyst": False,
        "N_Catalyst_Details": "",
        "S_Float_Tightness": False,
        "S_Float_Details": "",
        "I_Institutional_Quality": False,
        "I_Institutional_Details": "",
    }


def load_json_data(script_dir: str) -> Dict[str, Any]:
    enriched_path = os.path.join(script_dir, "enriched_canslim.json")
    intermediate_path = os.path.join(script_dir, "intermediate_canslim.json")

    if os.path.exists(enriched_path):
        logger.info("Loading AI-enriched data from %s", os.path.basename(enriched_path))
        path = enriched_path
    elif os.path.exists(intermediate_path):
        logger.info(
            "Enriched file not found; falling back to %s",
            os.path.basename(intermediate_path),
        )
        path = intermediate_path
    else:
        raise FileNotFoundError(
            "No CANSLIM JSON data files found. Run quantitative_analyzer.py first."
        )

    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_quantitative_metrics(quant: Dict[str, Any]) -> Dict[str, Any]:
    q = dict(quant or {})

    q.setdefault("C_Met", False)
    q.setdefault("A_Met", False)
    q.setdefault("L_Met", False)
    q.setdefault("C_Details", "")
    q.setdefault("A_Details", "")
    q.setdefault("Quarterly_EPS_Growth", None)
    q.setdefault("Annual_EPS_Growth", None)
    q.setdefault("EPS_Accelerating", False)
    q.setdefault("RS_Rating", 0.0)
    q.setdefault("Current_Price", 0.0)

    if "S_Quant_Met" not in q:
        q["S_Quant_Met"] = bool(q.get("S_Met", False))
    if "S_Quant_Details" not in q:
        q["S_Quant_Details"] = q.get("S_Details", "")
    if "I_Quant_Flag" not in q:
        q["I_Quant_Flag"] = bool(q.get("I_Met", False))
    if "I_Quant_Details" not in q:
        q["I_Quant_Details"] = q.get("I_Details", "")
    if "N_Technical_Met" not in q:
        q["N_Technical_Met"] = bool(q.get("N_Met", False))
    if "N_Technical_Details" not in q:
        q["N_Technical_Details"] = q.get("N_Details", "")

    q.setdefault("S_Score", 0)
    q.setdefault("Today_Volume_Strong", False)
    q.setdefault("Volume_Skew_Positive", False)
    q.setdefault("Near_52_Week_High", False)
    q.setdefault("Recent_Breakout", False)
    q.setdefault("Pct_From_High", None)
    q.setdefault("Float_Shares", None)
    q.setdefault("Institutional_Ownership", None)
    q.setdefault("High_52_Week", None)
    q.setdefault("Schema_Version", SCHEMA_VERSION)

    return q


def merge_ai_checks(stock: Dict[str, Any]) -> Dict[str, Any]:
    merged = default_ai_checks()
    pending = stock.get("AI_Qualitative_Checks_Pending", {}) or {}
    final_ai = stock.get("AI_Qualitative_Checks", {}) or {}

    merged.update(pending)
    merged.update(final_ai)
    return merged


def normalize_stock(stock: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "Ticker": stock.get("Ticker", ""),
        "Company_Name": stock.get("Company_Name", ""),
        "Quantitative_Metrics": normalize_quantitative_metrics(
            stock.get("Quantitative_Metrics", {})
        ),
        "AI_Qualitative_Checks_Pending": stock.get(
            "AI_Qualitative_Checks_Pending", {}
        )
        or {},
        "AI_Qualitative_Checks": merge_ai_checks(stock),
    }


def validate_dataset(data: Dict[str, Any]) -> None:
    if "Metadata" not in data or "Stocks" not in data:
        raise ValueError("Input JSON must contain 'Metadata' and 'Stocks'.")

    if not isinstance(data["Stocks"], list):
        raise ValueError("'Stocks' must be a list.")

    for index, stock in enumerate(data["Stocks"], start=1):
        if "Ticker" not in stock or "Company_Name" not in stock:
            raise ValueError(f"Stock #{index} is missing Ticker or Company_Name.")
        if "Quantitative_Metrics" not in stock:
            raise ValueError(f"Stock #{index} is missing Quantitative_Metrics.")


def calculate_score(
    stock: Dict[str, Any], m_is_uptrend: bool
) -> Tuple[int, List[str], List[str], Dict[str, Any]]:
    quant = stock["Quantitative_Metrics"]
    ai = stock["AI_Qualitative_Checks"]

    c_met = bool(quant.get("C_Met", False))
    a_met = bool(quant.get("A_Met", False))
    l_met = bool(quant.get("L_Met", False))

    n_met = bool(ai.get("N_New_Catalyst", False))
    s_met = bool(quant.get("S_Quant_Met", False)) and bool(
        ai.get("S_Float_Tightness", False)
    )
    i_met = bool(ai.get("I_Institutional_Quality", False))
    m_met = bool(m_is_uptrend)

    evaluations = {
        "C": c_met,
        "A": a_met,
        "N": n_met,
        "S": s_met,
        "L": l_met,
        "I": i_met,
        "M": m_met,
    }

    met = [name for name, passed in evaluations.items() if passed]
    missed = [name for name, passed in evaluations.items() if not passed]

    details = {
        "C_Details": quant.get("C_Details", ""),
        "A_Details": quant.get("A_Details", ""),
        "N_Catalyst_Details": ai.get("N_Catalyst_Details", ""),
        "N_Technical_Met": bool(quant.get("N_Technical_Met", False)),
        "N_Technical_Details": quant.get("N_Technical_Details", ""),
        "S_Quant_Met": bool(quant.get("S_Quant_Met", False)),
        "S_Quant_Details": quant.get("S_Quant_Details", ""),
        "S_Float_Tightness": bool(ai.get("S_Float_Tightness", False)),
        "S_Float_Details": ai.get("S_Float_Details", ""),
        "I_Quant_Flag": bool(quant.get("I_Quant_Flag", False)),
        "I_Quant_Details": quant.get("I_Quant_Details", ""),
        "I_Institutional_Quality": bool(ai.get("I_Institutional_Quality", False)),
        "I_Institutional_Details": ai.get("I_Institutional_Details", ""),
        "Quarterly_EPS_Growth": quant.get("Quarterly_EPS_Growth"),
        "Annual_EPS_Growth": quant.get("Annual_EPS_Growth"),
        "EPS_Accelerating": bool(quant.get("EPS_Accelerating", False)),
        "RS_Rating": quant.get("RS_Rating", 0.0),
        "Current_Price": quant.get("Current_Price", 0.0),
        "S_Score": quant.get("S_Score", 0),
        "Float_Shares": quant.get("Float_Shares"),
        "Institutional_Ownership": quant.get("Institutional_Ownership"),
        "Market_In_Confirmed_Uptrend": m_met,
    }

    return len(met), met, missed, details


def determine_grade(score: int) -> str:
    if score >= 7:
        return "A+"
    if score == 6:
        return "A"
    if score == 5:
        return "A-"
    if score == 4:
        return "B+"
    if score == 3:
        return "B"
    if score == 2:
        return "C"
    return "D"


def main() -> None:
    logger.info("--- Starting Fixed CANSLIM Final Processing ---")

    script_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        data = load_json_data(script_dir)
        validate_dataset(data)
    except Exception as exc:
        logger.error(str(exc))
        return

    metadata = data.get("Metadata", {})
    market_direction = metadata.get("Market_Direction_M", "Unknown")
    m_is_uptrend = market_direction == "Confirmed Uptrend"

    normalized_stocks = [normalize_stock(stock) for stock in data.get("Stocks", [])]
    if not normalized_stocks:
        logger.warning("No stocks found in input data. Nothing to process.")
        return

    processed_stocks: List[Dict[str, Any]] = []

    for stock in tqdm(normalized_stocks, desc="Compiling Final Scores", unit="stock"):
        try:
            score, met, missed, details = calculate_score(stock, m_is_uptrend)
            ai = stock["AI_Qualitative_Checks"]
            quant = stock["Quantitative_Metrics"]

            ai_note = (
                ai.get("N_Catalyst_Details")
                or quant.get("N_Technical_Details")
                or "No catalyst analysis available."
            )

            processed_stocks.append(
                {
                    "Ticker": stock["Ticker"],
                    "Company_Name": stock["Company_Name"],
                    "Final_Score": score,
                    "Grade": determine_grade(score),
                    "Met_Criteria": met,
                    "Missed_Criteria": missed,
                    "AI_Catalyst_Note": ai_note,
                    "Metrics": {
                        "RS_Rating": quant.get("RS_Rating", 0.0),
                        "Current_Price": quant.get("Current_Price", 0.0),
                        "Quarterly_EPS_Growth": quant.get("Quarterly_EPS_Growth"),
                        "Annual_EPS_Growth": quant.get("Annual_EPS_Growth"),
                        "EPS_Accelerating": bool(quant.get("EPS_Accelerating", False)),
                        "S_Score": quant.get("S_Score", 0),
                        "S_Quant_Met": bool(quant.get("S_Quant_Met", False)),
                        "S_Float_Tightness": bool(ai.get("S_Float_Tightness", False)),
                        "N_Technical_Met": bool(quant.get("N_Technical_Met", False)),
                        "Float_Shares": quant.get("Float_Shares"),
                        "Institutional_Ownership": quant.get(
                            "Institutional_Ownership"
                        ),
                    },
                    "Details": details,
                }
            )
        except Exception as exc:
            logger.error(
                "Error processing stock %s: %s",
                stock.get("Ticker", "Unknown"),
                exc,
            )

    processed_stocks.sort(
        key=lambda item: (item["Final_Score"], item["Metrics"]["RS_Rating"]),
        reverse=True,
    )

    score_distribution: Dict[str, int] = {}
    for stock in processed_stocks:
        score_key = str(stock["Final_Score"])
        score_distribution[score_key] = score_distribution.get(score_key, 0) + 1

    final_report = {
        "Schema_Version": SCHEMA_VERSION,
        "Report_Date": datetime.now().strftime("%Y-%m-%d"),
        "Report_Time": datetime.now().strftime("%H:%M:%S"),
        "Market_Environment": market_direction,
        "M_Criterion_Met": m_is_uptrend,
        "Total_Candidates_Evaluated": len(processed_stocks),
        "Score_Distribution": score_distribution,
        "Top_Candidates": processed_stocks,
        "Fixes_Applied": metadata.get("Fixes_Applied", []),
    }

    output_path = os.path.join(script_dir, "final_canslim_report.json")
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(final_report, handle, indent=4)

    logger.info("Market Environment: %s", market_direction)
    logger.info("Total stocks evaluated: %s", len(processed_stocks))
    logger.info("Score distribution: %s", score_distribution)
    logger.info("Results saved to: %s", output_path)

    # Generate PDF report
    try:
        pdf_generator_path = os.path.join(script_dir, "pdf_report_generator.py")
        if os.path.exists(pdf_generator_path):
            logger.info("Generating PDF report...")
            result = subprocess.run(
                [sys.executable, pdf_generator_path],
                cwd=script_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                logger.info("PDF report generated successfully")
            else:
                logger.warning("PDF generation failed: %s", result.stderr)
        else:
            logger.warning("PDF generator script not found: %s", pdf_generator_path)
    except Exception as exc:
        logger.warning("Error generating PDF report: %s", exc)


if __name__ == "__main__":
    main()
