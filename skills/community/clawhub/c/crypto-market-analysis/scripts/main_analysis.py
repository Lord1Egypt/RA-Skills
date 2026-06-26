import requests
import json
import sys
import subprocess
import os
import site
import numpy as np # Import numpy to handle its types

# Explicitly define the Python executable path found earlier
PYTHON_EXECUTABLE = "E:\\anaconda\\python.exe"

# Assuming get_binance_data.py and calculate_indicators.py are in the same directory as this script
SCRIPT_DIR = os.path.dirname(__file__)
GET_BINANCE_DATA_SCRIPT = os.path.join(SCRIPT_DIR, 'get_binance_data.py')
CALCULATE_INDICATORS_SCRIPT = os.path.join(SCRIPT_DIR, 'calculate_indicators.py')

def get_current_price_and_24hr_stats(symbol):
    base_url = "https://api.binance.com/api/v3/ticker/24hr"
    params = {
        "symbol": symbol.upper()
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        
        return {
            "current_price": float(data.get("lastPrice")),
            "price_change_percent": float(data.get("priceChangePercent")),
            "high_price_24hr": float(data.get("highPrice")),
            "low_price_24hr": float(data.get("lowPrice")),
            "quote_volume_24hr": float(data.get("quoteVolume")) # This is the volume in terms of the quote asset (e.g., USDT)
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching 24hr ticker for {symbol}: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred fetching 24hr ticker: {e}"}

def install_ta_lib():
    try:
        # Attempt to import TA-Lib using the explicitly defined PYTHON_EXECUTABLE
        result = subprocess.run(
            [PYTHON_EXECUTABLE, "-c", "import talib"],
            capture_output=True, text=True, check=False # Don't check=True initially, as it might not be installed
        )
        if result.returncode == 0:
            print("TA-Lib is already installed.", file=sys.stderr)
            return True
        else:
            print("TA-Lib not found. Attempting to install TA-Lib...", file=sys.stderr)
            # Use pip to install TA-Lib. Use the explicit Python executable.
            subprocess.run([PYTHON_EXECUTABLE, "-m", "pip", "install", "TA-Lib"], check=True, capture_output=True)
            print("TA-Lib installed successfully.", file=sys.stderr)
            return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing TA-Lib: {e.stderr}", file=sys.stderr)
        print("Please install TA-Lib manually using: pip install TA-Lib", file=sys.stderr)
        return False
    except Exception as e:
        print(f"An unexpected error occurred during TA-Lib installation: {e}", file=sys.stderr)
        return False

def convert_numpy_to_float(obj):
    # Recursively convert numpy types to standard Python types for JSON serialization
    if isinstance(obj, np.float64) or isinstance(obj, np.int64):
        return float(obj) # Convert all numpy numerical types to float
    elif isinstance(obj, dict):
        return {k: convert_numpy_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_to_float(elem) for elem in obj]
    else:
        return obj

def format_report(report_data, llm_analysis):
    # Basic Info
    basic_info = report_data["basic_info"]
    formatted_report = f"""### {report_data["symbol"]} 行情分析報告

#### 1. 基本資訊
- **當前價格**: ${basic_info.get("current_price", "N/A")}{':,.2f' if isinstance(basic_info.get("current_price"), (int, float)) else ''}
- **24小時變化百分比**: {basic_info.get("24h_change_percent", "N/A")}{'.2f%' if isinstance(basic_info.get("24h_change_percent"), (int, float)) else ''}
- **24小時最高價**: ${basic_info.get("24h_high", "N/A")}{':,.2f' if isinstance(basic_info.get("24h_high"), (int, float)) else ''}
- **24小時最低價**: ${basic_info.get("low_price_24hr", "N/A")}{':,.2f' if isinstance(basic_info.get("low_price_24hr"), (int, float)) else ''}
- **24小時交易量 (USDT)**: {basic_info.get("quote_volume_24hr", "N/A")}{':,.2f' if isinstance(basic_info.get("quote_volume_24hr"), (int, float)) else ''}

"""

    # Short Term Indicators
    short_term = report_data["short_term_indicators"]
    formatted_report += f"""#### 2. 短期技術指標分析 ({report_data["short_term_interval"]})
"""
    if short_term and "error" not in short_term:
        formatted_report += f"- **MACD**: MACD({short_term.get('MACD', {}).get('MACD', 'N/A')}), DIFF({short_term.get('MACD', {}).get('DIFF', 'N/A')}), DEA({short_term.get('MACD', {}).get('DEA', 'N/A')})\n"
        formatted_report += f"- **KDJ**: K({short_term.get('KDJ', {}).get('K', 'N/A')}), D({short_term.get('KDJ', {}).get('D', 'N/A')}), J({short_term.get('KDJ', {}).get('J', 'N/A')})\n"
        formatted_report += f"- **RSI**: RSI_6({short_term.get('RSI', {}).get('RSI_6', 'N/A')}), RSI_12({short_term.get('RSI', {}).get('RSI_12', 'N/A')}), RSI_24({short_term.get('RSI', {}).get('RSI_24', 'N/A')})\n"
        formatted_report += f"- **CCI**: {short_term.get('CCI', 'N/A')}\n"
        formatted_report += f"- **BOLL**: 上軌({short_term.get('BOLL', {}).get('Upper', 'N/A')}), 中軌({short_term.get('BOLL', {}).get('Middle', 'N/A')}), 下軌({short_term.get('BOLL', {}).get('Lower', 'N/A')})\n"
        formatted_report += f"- **WR**: {short_term.get('WR', 'N/A')}\n"
        formatted_report += f"- **PSY**: PSY_12({short_term.get('PSY', {}).get('PSY_12', 'N/A')}), PSY_6({short_term.get('PSY', {}).get('PSY_6', 'N/A')})\n"
        formatted_report += f"- **BRAR**: BR({short_term.get('BRAR', {}).get('BR', 'N/A')}), AR({short_term.get('BRAR', {}).get('AR', 'N/A')})\n"
        formatted_report += f"- **DMI**: ADX({short_term.get('DMI', {}).get('ADX', 'N/A')}), DI_Minus({short_term.get('DMI', {}).get('DI_Minus', 'N/A')}), DI_Plus({short_term.get('DMI', {}).get('DI_Plus', 'N/A')})\n"
    elif "error" in short_term:
        formatted_report += f"- 短期指标计算失败：{short_term["error"]}\n"
    else:
        formatted_report += "- 无可用短期指标数据。\n"

    # Long Term Indicators
    long_term = report_data["long_term_indicators"]
    formatted_report += f"""
#### 3. 中長期技術指標分析 ({report_data["long_term_interval"]})
"""
    if long_term and "error" not in long_term:
        formatted_report += f"- **MACD**: MACD({long_term.get('MACD', {}).get('MACD', 'N/A')}), DIFF({long_term.get('MACD', {}).get('DIFF', 'N/A')}), DEA({long_term.get('MACD', {}).get('DEA', 'N/A')})\n"
        formatted_report += f"- **KDJ**: K({long_term.get('KDJ', {}).get('K', 'N/A')}), D({long_term.get('KDJ', {}).get('D', 'N/A')}), J({long_term.get('KDJ', {}).get('J', 'N/A')})\n"
        formatted_report += f"- **RSI**: RSI_6({long_term.get('RSI', {}).get('RSI_6', 'N/A')}), RSI_12({long_term.get('RSI', {}).get('RSI_12', 'N/A')}), RSI_24({long_term.get('RSI', {}).get('RSI_24', 'N/A')})\n"
        formatted_report += f"- **CCI**: {long_term.get('CCI', 'N/A')}\n"
        formatted_report += f"- **BOLL**: 上軌({long_term.get('BOLL', {}).get('Upper', 'N/A')}), 中軌({long_term.get('BOLL', {}).get('Middle', 'N/A')}), 下軌({long_term.get('BOLL', {}).get('Lower', 'N/A')})\n"
        formatted_report += f"- **WR**: {long_term.get('WR', 'N/A')}\n"
        formatted_report += f"- **PSY**: PSY_12({long_term.get('PSY', {}).get('PSY_12', 'N/A')}), PSY_6({long_term.get('PSY', {}).get('PSY_6', 'N/A')})\n"
        formatted_report += f"- **BRAR**: BR({long_term.get('BRAR', {}).get('BR', 'N/A')}), AR({long_term.get('BRAR', {}).get('AR', 'N/A')})\n"
        formatted_report += f"- **DMI**: ADX({long_term.get('DMI', {}).get('ADX', 'N/A')}), DI_Minus({long_term.get('DMI', {}).get('DI_Minus', 'N/A')}), DI_Plus({long_term.get('DMI', {}).get('DI_Plus', 'N/A')})\n"
    elif "error" in long_term:
        formatted_report += f"- 中长期指标计算失败：{long_term["error"]}\n"
    else:
        formatted_report += "- 无可用中长期指标数据。\n"

    # LLM Analysis
    formatted_report += f"""
#### 4. 總結與建議
{llm_analysis}

請根據自身的風險承受能力，制定相應的交易策略。如需進一步的操作建議，歡迎隨時咨詢！
"""
    return formatted_report

def run_analysis(symbol, short_term_interval="1h", long_term_interval="1d"):
    report_data = {
        "symbol": symbol.upper(),
        "short_term_interval": short_term_interval,
        "long_term_interval": long_term_interval,
        "basic_info": {},
        "short_term_indicators": {},
        "long_term_indicators": {},
    }
    
    # Ensure TA-Lib is installed
    if not install_ta_lib():
        # If TA-Lib installation failed, we cannot proceed with indicator calculation.
        # Set error messages and continue to generate LLM prompt with available data.
        report_data["short_term_indicators"] = {"error": "TA-Lib installation failed or not found."}
        report_data["long_term_indicators"] = {"error": "TA-Lib installation failed or not found."}
    

    # Prepare environment for subprocesses to ensure Python path is correct
    env_for_subprocess = os.environ.copy()
    python_path_extra = os.pathsep.join(site.getsitepackages()) # Get all site-packages paths
    if "PYTHONPATH" in env_for_subprocess:
        env_for_subprocess["PYTHONPATH"] = python_path_extra + os.pathsep + env_for_subprocess["PYTHONPATH"]
    else:
        env_for_subprocess["PYTHONPATH"] = python_path_extra
    
    # Also add the script directory to PYTHONPATH for custom scripts
    if SCRIPT_DIR not in env_for_subprocess["PYTHONPATH"]:
        env_for_subprocess["PYTHONPATH"] = SCRIPT_DIR + os.pathsep + env_for_subprocess["PYTHONPATH"]

    # Explicitly set PYTHONHOME and PYTHONSTARTUP for consistency (common for embedded Python)
    # This often helps in finding platform independent libraries
    # For Anaconda, PYTHONHOME is usually the Anaconda root directory
    # Since PYTHON_EXECUTABLE is E:\anaconda\python.exe, PYTHONHOME should be E:\anaconda
    env_for_subprocess["PYTHONHOME"] = os.path.dirname(PYTHON_EXECUTABLE) # E:\anaconda
    env_for_subprocess["PYTHONSTARTUP"] = "" # Clear it to avoid issues


    # 1. Get Basic Info from 24hr ticker
    basic_stats = get_current_price_and_24hr_stats(symbol + "USDT") 
    if basic_stats and "error" not in basic_stats:
        report_data["basic_info"] = {
            "current_price": basic_stats["current_price"],
            "24h_change_percent": basic_stats["price_change_percent"],
            "24h_high": basic_stats["high_price_24hr"],
            "24h_low": basic_stats["low_price_24hr"],
            "quote_volume_24hr": basic_stats["quote_volume_24hr"],
        }
    else:
        print(f"Warning: Could not retrieve basic info for {symbol}. Error: {basic_stats.get('error', 'Unknown error')}", file=sys.stderr)
        report_data["basic_info"] = {
            "current_price": "N/A", "24h_change_percent": "N/A", "24h_high": "N/A", "24h_low": "N/A",
            "quote_volume_24hr": "N/A", 
        }

    # 2. Get Klines and Calculate Indicators for Short Term
    # Only attempt if TA-Lib was successfully installed or no error in initial check
    if "error" not in report_data.get("short_term_indicators", {}):
        try:
            klines_short_process = subprocess.run(
                [PYTHON_EXECUTABLE, GET_BINANCE_DATA_SCRIPT, symbol + "USDT", short_term_interval, "500"],
                capture_output=True, text=True, check=False, env=env_for_subprocess # check=False here
            )
            # IMPORTANT: Check return code and stderr/stdout here
            if klines_short_process.returncode != 0:
                error_msg = klines_short_process.stderr or klines_short_process.stdout or f"Process exited with code {klines_short_process.returncode}"
                raise subprocess.CalledProcessError(returncode=klines_short_process.returncode, cmd=klines_short_process.args, stderr=error_msg)
            
            short_klines_data = json.loads(klines_short_process.stdout)
            
            indicators_short_process = subprocess.run(
                [PYTHON_EXECUTABLE, CALCULATE_INDICATORS_SCRIPT],
                input=json.dumps(short_klines_data), capture_output=True, text=True, check=False, env=env_for_subprocess # check=False here
            )
            # IMPORTANT: Check return code and stderr/stdout here
            if indicators_short_process.returncode != 0:
                error_msg = indicators_short_process.stderr or indicators_short_process.stdout or f"Process exited with code {indicators_short_process.returncode}"
                raise subprocess.CalledProcessError(returncode=indicators_short_process.returncode, cmd=indicators_short_process.args, stderr=error_msg)

            # Convert numpy types to standard Python types for JSON compatibility
            report_data["short_term_indicators"] = convert_numpy_to_float(json.loads(indicators_short_process.stdout))

        except subprocess.CalledProcessError as e:
            print(f"Error during short-term data processing: {e.stderr}", file=sys.stderr)
            report_data["short_term_indicators"] = {"error": f"Short-term indicator calculation failed: {e.stderr}"}
        except json.JSONDecodeError as e:
            print(f"JSON decode error in short-term processing: {e}. Output: {klines_short_process.stdout}", file=sys.stderr)
            report_data["short_term_indicators"] = {"error": f"Short-term indicator JSON decode failed: {e}. Output: {klines_short_process.stdout}"}
        except FileNotFoundError:
            print(f"Error: Python script not found. Make sure '{GET_BINANCE_DATA_SCRIPT}' and '{CALCULATE_INDICATORS_SCRIPT}' exist.", file=sys.stderr)
            report_data["short_term_indicators"] = {"error": "Script not found for short-term processing."}


    # 3. Get Klines and Calculate Indicators for Long Term
    # Only attempt if TA-Lib was successfully installed or no error in initial check
    if "error" not in report_data.get("long_term_indicators", {}):
        try:
            klines_long_process = subprocess.run(
                [PYTHON_EXECUTABLE, GET_BINANCE_DATA_SCRIPT, symbol + "USDT", long_term_interval, "500"],
                capture_output=True, text=True, check=False, env=env_for_subprocess # check=False here
            )
            # IMPORTANT: Check return code and stderr/stdout here
            if klines_long_process.returncode != 0:
                error_msg = klines_long_process.stderr or klines_long_process.stdout or f"Process exited with code {klines_long_process.returncode}"
                raise subprocess.CalledProcessError(returncode=klines_long_process.returncode, cmd=klines_long_process.args, stderr=error_msg)

            long_klines_data = json.loads(klines_long_process.stdout)

            indicators_long_process = subprocess.run(
                [PYTHON_EXECUTABLE, CALCULATE_INDICATORS_SCRIPT],
                input=json.dumps(long_klines_data), capture_output=True, text=True, check=False, env=env_for_subprocess # check=False here
            )
            # IMPORTANT: Check return code and stderr/stdout here
            if indicators_long_process.returncode != 0:
                error_msg = indicators_long_process.stderr or indicators_long_process.stdout or f"Process exited with code {indicators_long_process.returncode}"
                raise subprocess.CalledProcessError(returncode=indicators_long_process.returncode, cmd=indicators_long_process.args, stderr=error_msg)

            # Convert numpy types to standard Python types for JSON compatibility
            report_data["long_term_indicators"] = convert_numpy_to_float(json.loads(indicators_long_process.stdout))

        except subprocess.CalledProcessError as e:
            print(f"Error during long-term data processing: {e.stderr}", file=sys.stderr)
            report_data["long_term_indicators"] = {"error": f"Long-term indicator calculation failed: {e.stderr}"}
        except json.JSONDecodeError as e:
            print(f"JSON decode error in long-term processing: {e}. Output: {klines_long_process.stdout}", file=sys.stderr)
            report_data["long_term_indicators"] = {"error": f"Long-term indicator JSON decode failed: {e}. Output: {klines_long_process.stdout}"}
        except FileNotFoundError:
            print(f"Error: Python script not found. Make sure '{GET_BINANCE_DATA_SCRIPT}' and '{CALCULATE_INDICATORS_SCRIPT}' exist.", file=sys.stderr)
            report_data["long_term_indicators"] = {"error": "Script not found for long-term processing."}

    # 4. Generate LLM Prompt
    # Now, ensure all basic info numbers are formatted BEFORE being embedded into the LLM prompt
    formatted_basic_info = {
        "current_price": f"{report_data["basic_info"].get("current_price", "N/A"):,.2f}" if isinstance(report_data["basic_info"].get("current_price"), (int, float)) else "N/A",
        "24h_change_percent": f"{report_data["basic_info"].get("24h_change_percent", "N/A"):.2f}%" if isinstance(report_data["basic_info"].get("24h_change_percent"), (int, float)) else "N/A",
        "24h_high": f"{report_data["basic_info"].get("24h_high", "N/A"):,.2f}" if isinstance(report_data["basic_info"].get("24h_high"), (int, float)) else "N/A",
        "24h_low": f"{report_data["basic_info"].get("low_price_24hr", "N/A"):,.2f}" if isinstance(report_data["basic_info"].get("low_price_24hr"), (int, float)) else "N/A",
        "quote_volume_24hr": f"{report_data["basic_info"].get("quote_volume_24hr", "N/A"):,.2f}" if isinstance(report_data["basic_info"].get("quote_volume_24hr"), (int, float)) else "N/A",
    }

    llm_prompt = f"""
    你是一个专业的加密货币市场分析师，请根据以下提供的实时行情数据和技术指标，对 {report_data["symbol"]} 进行全面的市场分析，并给出总结和投资建议。分析应考虑短期和中长期趋势，并结合您对市场情绪和风险的理解。

    请严格按照以下结构输出中文分析报告。如果某些数据缺失，请在报告中显示 'N/A' 或进行合理推断。

    ### {report_data["symbol"]} 行情分析報告

    #### 1. 基本資訊
    - **當前價格**: ${formatted_basic_info["current_price"]}
    - **24小時變化百分比**: {formatted_basic_info["24h_change_percent"]}
    - **24小時最高價**: ${formatted_basic_info["24h_high"]}
    - **24小時最低價**: ${formatted_basic_info["24h_low"]}
    - **24小時交易量 (USDT)**: {formatted_basic_info["quote_volume_24hr"]}

    #### 2. 短期技術指標分析 ({report_data["short_term_interval"]})
    MACD: {report_data["short_term_indicators"].get('MACD', '指标计算失败')}
    KDJ: {report_data["short_term_indicators"].get('KDJ', '指标计算失败')}
    RSI: {report_data["short_term_indicators"].get('RSI', '指标计算失败')}
    CCI: {report_data["short_term_indicators"].get('CCI', '指标计算失败')}
    BOLL: {report_data["short_term_indicators"].get('BOLL', '指标计算失败')}
    WR: {report_data["short_term_indicators"].get('WR', '指标计算失败')}
    PSY: {report_data["short_term_indicators"].get('PSY', '指标计算失败')}
    BRAR: {report_data["short_term_indicators"].get('BRAR', '指标计算失败')}
    DMI: {report_data["short_term_indicators"].get('DMI', '指标计算失败')}

    #### 3. 中長期技術指標分析 ({report_data["long_term_interval"]})
    MACD: {report_data["long_term_indicators"].get('MACD', '指标计算失败')}
    KDJ: {report_data["long_term_indicators"].get('KDJ', '指标计算失败')}
    RSI: {report_data["long_term_indicators"].get('RSI', '指标计算失败')}
    CCI: {report_data["long_term_indicators"].get('CCI', '指标计算失败')}
    BOLL: {report_data["long_term_indicators"].get('BOLL', '指标计算失败')}
    WR: {report_data["long_term_indicators"].get('WR', '指标计算失败')}
    PSY: {report_data["long_term_indicators"].get('PSY', '指标计算失败')}
    BRAR: {report_data["long_term_indicators"].get('BRAR', '指标计算失败')}
    DMI: {report_data["long_term_indicators"].get('DMI', '指标计算失败')}

    #### 4. 總結與建議
    请根据上述数据，生成一份专业的市场分析和投资建议。
    """
    return llm_prompt, report_data # Return prompt and data to agent for LLM call

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: py main_analysis.py <symbol> [short_interval] [long_interval]"}), file=sys.stderr)
        sys.exit(1)
    
    symbol_to_analyze = sys.argv[1]
    short_interval = sys.argv[2] if len(sys.argv) > 2 else "1h"
    long_interval = sys.argv[3] if len(sys.argv) > 3 else "1d"
    
    try:
        llm_prompt, report_data = run_analysis(symbol_to_analyze, short_interval, long_interval)
        # The agent will capture this JSON output
        print(json.dumps({
            "status": "ready_for_llm",
            "llm_prompt": llm_prompt,
            "report_data": report_data
        }))
    except Exception as e:
        print(json.dumps({"error": f"An unexpected error occurred in main_analysis.py: {e}"}), file=sys.stderr)
        sys.exit(1)
