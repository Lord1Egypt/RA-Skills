# Python Script Catalog

Extracted from Appendix A. Each item has an executable or near-executable source file in `assets/python-scripts/`.

## Topic Taxonomy

#### Appendix A: 100 Fully Implemented python scripts examples for Electrical Engineers
Scripts 1–10 (Fundamentals)
Power Calculator
Calculates electrical power using voltage and current inputs.
Load Forecasting Model
Uses linear regression to predict future electrical load demand.
Transformer Efficiency Calculator
Computes efficiency based on input and output power.
Fault Classification Model
Applies basic machine learning to classify electrical faults.
Data Cleaner
Removes missing values and prepares datasets for analysis.
Signal Plotter
Visualizes voltage or current signals over time.
Unit Converter
Converts electrical quantities between units (W, kW, MW).
Prompt Validator
Evaluates the quality of engineering prompts.
Ohm’s Law Solver
Calculates voltage, current, or resistance.
Voltage Drop Calculator
Computes voltage drop across a conductor.
🔹 Scripts 11–20 (Tools & Data Handling)
CSV Data Reader
Loads and summarizes engineering datasets from CSV files.
AC Signal Plotter
Generates and visualizes sinusoidal waveforms.
Advanced Unit Converter
Handles multiple electrical unit conversions.
Result Comparator
Compares calculated and reference data for accuracy.
Report Generator
Creates formatted engineering reports from results.
JSON Circuit Loader
Loads circuit parameters from structured JSON files.
Prompt Logger
Stores prompts for reuse in engineering workflows.
Excel Data Import Tool
Imports electrical data from Excel spreadsheets.
Batch Calculation Tool
Performs multiple electrical calculations simultaneously.
Notebook Template Generator
Creates structured templates for engineering analysis.
🔹 Scripts 21–30 (Prompt Engineering)
Prompt Quality Analyzer
Scores prompts based on clarity and completeness.
Prompt Library Manager
Stores and organizes engineering prompts.
Prompt Rewriter
Improves weak prompts into professional ones.
Prompt-to-Code Generator
Converts tasks into code-generation prompts.
Prompt Categorizer
Classifies prompts into engineering domains.
Prompt Usage Analyzer
Tracks frequency of prompt usage.
Interview Question Generator
Generates technical interview questions.
Relay Study Prompt Generator
Creates prompts for protection studies.
Prompt Export Tool
Exports prompts into CSV format.
Prompt Performance Tracker
Ranks prompts based on effectiveness.
🔹 Scripts 31–40 (Electrical Calculations)
Advanced Ohm’s Law Solver
Enhanced version supporting unknown variable solving.
Power Triangle Calculator
Calculates real, reactive, and apparent power.
Voltage Drop with Distance
Computes voltage drop considering cable length.
Three-Phase Power Calculator
Calculates three-phase electrical power.
Transformer Ratio Calculator
Determines secondary voltage from turns ratio.
Cable Sizing Tool
Suggests cable size based on load current.
Resistance Network Solver
Calculates equivalent resistance in circuits.
Capacitor Energy Calculator
Computes stored energy in capacitors.
RL Time Constant Calculator
Calculates circuit time constant.
Parameter Sweep Plotter
Analyzes system behavior over variable ranges.
🔹 Scripts 41–50 (Power Systems & Smart Grids)
Load Forecasting Tool
Predicts future demand using historical data.
Peak Load Detector
Identifies maximum load in a dataset.
Voltage Profile Plotter
Visualizes voltage across power system buses.
Transmission Loss Calculator
Computes I²R losses in lines.
Short Circuit Calculator
Estimates fault current.
Renewable Penetration Calculator
Measures renewable contribution to grid.
Load Factor Calculator
Calculates system utilization efficiency.
Smart Meter Aggregator
Summarizes energy consumption data.
Wind Power Estimator
Estimates wind energy output.
Solar Power Calculator
Computes solar generation output.
🔹 Scripts 51–60 (Design & Protection)
Voltage Divider Designer
Designs resistor values for voltage division.
LED Resistor Calculator
Calculates current-limiting resistor for LEDs.
Motor Starter Selector
Recommends motor starting methods.
Circuit Breaker Selector
Determines appropriate breaker rating.
Power Factor Correction Tool
Calculates required capacitor size.
Transformer Sizing Tool
Determines required transformer rating.
Relay Pickup Calculator
Calculates relay settings.
Ground Resistance Estimator
Estimates grounding system resistance.
Battery Backup Calculator
Estimates backup duration.
Single-Line Data Generator
Generates structured system data.
🔹 Scripts 61–70 (AI Workflows & Prompt Systems)
Power System Prompt Generator
Creates domain-specific prompts.
ETAP Prompt Manager
Organizes simulation prompts.
MATLAB Prompt Generator
Generates prompts for MATLAB scripting.
Advanced Report Generator
Creates structured engineering reports.
Prompt Search Tool
Finds prompts using keywords.
Prompt Similarity Checker
Measures similarity between prompts.
Prompt Tagging Tool
Assigns categories to prompts.
Prompt Version Tracker
Tracks prompt revisions.
Prompt Metadata Extractor
Extracts structural elements from prompts.
Prompt Benchmark Tool
Evaluates prompt effectiveness.
🔹 Scripts 71–80 (Career Toolkit)
Resume Analyzer
Evaluates keyword coverage in resumes.
Skills Gap Analyzer
Identifies missing skills.
Interview Question Bank
Provides practice questions.
Mock Interview Scorer
Tracks interview performance.
Portfolio Tracker
Organizes engineering projects.
Certification Tracker
Tracks professional certifications.
Study Schedule Generator
Creates learning plans.
Job Tracker
Tracks job applications.
Salary Comparison Tool
Analyzes salary offers.
LinkedIn Optimizer
Suggests profile improvements.
🔹 Scripts 81–90 (Data Analysis & Visualization)
Load Curve Plotter
Visualizes demand variation over time.
Voltage Trend Analyzer
Tracks voltage fluctuations.
Harmonic Analyzer
Displays harmonic content.
Anomaly Detector
Identifies abnormal readings.
Power Quality Monitor
Checks voltage, frequency, and harmonics.
Correlation Analyzer
Finds relationships between variables.
Missing Data Filler
Interpolates missing values.
Substation Monitor
Tracks system performance.
Energy Breakdown Chart
Shows energy usage distribution.
Real-Time Data Simulator
Simulates live system data.
🔹 Scripts 91–100 (Optimization & Decision Systems)
Loss Optimization Tool
Minimizes transmission losses.
Economic Load Dispatch Tool
Optimizes generator usage.
Capacitor Placement Tool
Improves voltage stability.
Battery Dispatch Optimizer
Optimizes energy storage use.
Renewable Mix Optimizer
Optimizes energy sources.
Transformer Load Balancer
Balances system loads.
Voltage Setpoint Optimizer
Optimizes voltage levels.
Multi-Criteria Decision Tool
Evaluates engineering options.
Maintenance Scheduler
Prioritizes maintenance tasks.
Decision Support System
Selects best engineering solution.
### Script 1 — Power Calculator

## Extracted Script Files

- 001. Power Calculator -> `assets/python-scripts/script_001_power_calculator.py`
- 002. Load Forecasting (Linear Regression) -> `assets/python-scripts/script_002_load_forecasting_linear_regression.py`
- 003. Transformer Efficiency -> `assets/python-scripts/script_003_transformer_efficiency.py`
- 004. Fault Classification (Simple ML) -> `assets/python-scripts/script_004_fault_classification_simple_ml.py`
- 005. Data Cleaner -> `assets/python-scripts/script_005_data_cleaner.py`
- 006. Signal Plotter -> `assets/python-scripts/script_006_signal_plotter.py`
- 007. Unit Converter -> `assets/python-scripts/script_007_unit_converter.py`
- 008. Prompt Validator -> `assets/python-scripts/script_008_prompt_validator.py`
- 009. Ohm’s Law Solver -> `assets/python-scripts/script_009_ohm_s_law_solver.py`
- 010. Voltage Drop Calculator -> `assets/python-scripts/script_010_voltage_drop_calculator.py`
- 011. CSV Engineering Data Reader -> `assets/python-scripts/script_011_csv_engineering_data_reader.py`
- 012. Signal Plotter (Improved) -> `assets/python-scripts/script_012_signal_plotter_improved.py`
- 013. Electrical Unit Converter (Full) -> `assets/python-scripts/script_013_electrical_unit_converter_full.py`
- 014. Power System Result Comparator -> `assets/python-scripts/script_014_power_system_result_comparator.py`
- 015. Engineering Report Generator -> `assets/python-scripts/script_015_engineering_report_generator.py`
- 016. JSON Circuit Loader -> `assets/python-scripts/script_016_json_circuit_loader.py`
- 017. Prompt Logger -> `assets/python-scripts/script_017_prompt_logger.py`
- 018. Excel Sensor Data Import -> `assets/python-scripts/script_018_excel_sensor_data_import.py`
- 019. Batch Formula Evaluator -> `assets/python-scripts/script_019_batch_formula_evaluator.py`
- 020. Engineering Notebook Starter -> `assets/python-scripts/script_020_engineering_notebook_starter.py`
- 021. Prompt Quality Analyzer (Advanced) -> `assets/python-scripts/script_021_prompt_quality_analyzer_advanced.py`
- 022. Prompt Library Manager -> `assets/python-scripts/script_022_prompt_library_manager.py`
- 023. Prompt Rewriter -> `assets/python-scripts/script_023_prompt_rewriter.py`
- 024. Prompt-to-Code Generator -> `assets/python-scripts/script_024_prompt_to_code_generator.py`
- 025. Prompt Categorizer -> `assets/python-scripts/script_025_prompt_categorizer.py`
- 026. Prompt Usage Analyzer -> `assets/python-scripts/script_026_prompt_usage_analyzer.py`
- 027. Interview Question Generator -> `assets/python-scripts/script_027_interview_question_generator.py`
- 028. Relay Study Prompt Generator -> `assets/python-scripts/script_028_relay_study_prompt_generator.py`
- 029. Prompt Export to CSV -> `assets/python-scripts/script_029_prompt_export_to_csv.py`
- 030. Prompt Performance Tracker -> `assets/python-scripts/script_030_prompt_performance_tracker.py`
- 031. Ohm’s Law Full Solver (Improved) -> `assets/python-scripts/script_031_ohm_s_law_full_solver_improved.py`
- 032. Power Triangle Calculator -> `assets/python-scripts/script_032_power_triangle_calculator.py`
- 033. Voltage Drop with Distance -> `assets/python-scripts/script_033_voltage_drop_with_distance.py`
- 034. Three-Phase Power Calculator -> `assets/python-scripts/script_034_three_phase_power_calculator.py`
- 035. Transformer Turns Ratio -> `assets/python-scripts/script_035_transformer_turns_ratio.py`
- 036. Cable Sizing (Basic) -> `assets/python-scripts/script_036_cable_sizing_basic.py`
- 037. Resistance Network Solver -> `assets/python-scripts/script_037_resistance_network_solver.py`
- 038. Capacitor Energy Storage -> `assets/python-scripts/script_038_capacitor_energy_storage.py`
- 039. RL Time Constant -> `assets/python-scripts/script_039_rl_time_constant.py`
- 040. Parameter Sweep Plot -> `assets/python-scripts/script_040_parameter_sweep_plot.py`
- 041. Load Forecasting (Linear Regression – Practical) -> `assets/python-scripts/script_041_load_forecasting_linear_regression_practical.py`
- 042. Peak Load Detector -> `assets/python-scripts/script_042_peak_load_detector.py`
- 043. Bus Voltage Profile Plot -> `assets/python-scripts/script_043_bus_voltage_profile_plot.py`
- 044. Transmission Line Loss Calculator -> `assets/python-scripts/script_044_transmission_line_loss_calculator.py`
- 045. Short Circuit Current Calculator -> `assets/python-scripts/script_045_short_circuit_current_calculator.py`
- 046. Renewable Penetration Calculator -> `assets/python-scripts/script_046_renewable_penetration_calculator.py`
- 047. Load Factor Calculator -> `assets/python-scripts/script_047_load_factor_calculator.py`
- 048. Smart Meter Data Aggregator -> `assets/python-scripts/script_048_smart_meter_data_aggregator.py`
- 049. Wind Power Estimator -> `assets/python-scripts/script_049_wind_power_estimator.py`
- 050. Solar Power Calculator -> `assets/python-scripts/script_050_solar_power_calculator.py`
- 051. Voltage Divider Designer -> `assets/python-scripts/script_051_voltage_divider_designer.py`
- 052. LED Resistor Calculator -> `assets/python-scripts/script_052_led_resistor_calculator.py`
- 053. Motor Starter Sizing -> `assets/python-scripts/script_053_motor_starter_sizing.py`
- 054. Circuit Breaker Selection -> `assets/python-scripts/script_054_circuit_breaker_selection.py`
- 055. Power Factor Correction -> `assets/python-scripts/script_055_power_factor_correction.py`
- 056. Transformer Sizing -> `assets/python-scripts/script_056_transformer_sizing.py`
- 057. Relay Pickup Setting -> `assets/python-scripts/script_057_relay_pickup_setting.py`
- 058. Ground Resistance Estimate -> `assets/python-scripts/script_058_ground_resistance_estimate.py`
- 059. Battery Backup Calculator -> `assets/python-scripts/script_059_battery_backup_calculator.py`
- 060. Single-Line Data Generator -> `assets/python-scripts/script_060_single_line_data_generator.py`
- 061. Power System Prompt Pack Generator -> `assets/python-scripts/script_061_power_system_prompt_pack_generator.py`
- 062. ETAP Modeling Prompt Manager -> `assets/python-scripts/script_062_etap_modeling_prompt_manager.py`
- 063. MATLAB Script Prompt Generator -> `assets/python-scripts/script_063_matlab_script_prompt_generator.py`
- 064. Engineering Report Generator (Advanced) -> `assets/python-scripts/script_064_engineering_report_generator_advanced.py`
- 065. Prompt Search Tool -> `assets/python-scripts/script_065_prompt_search_tool.py`
- 066. Prompt Similarity Checker -> `assets/python-scripts/script_066_prompt_similarity_checker.py`
- 067. Prompt Tagging System -> `assets/python-scripts/script_067_prompt_tagging_system.py`
- 068. Prompt Version Tracker -> `assets/python-scripts/script_068_prompt_version_tracker.py`
- 069. Prompt Metadata Extractor -> `assets/python-scripts/script_069_prompt_metadata_extractor.py`
- 070. Prompt Benchmarking Tool -> `assets/python-scripts/script_070_prompt_benchmarking_tool.py`
- 071. Resume Keyword Analyzer -> `assets/python-scripts/script_071_resume_keyword_analyzer.py`
- 072. Skills Gap Analyzer -> `assets/python-scripts/script_072_skills_gap_analyzer.py`
- 073. Interview Question Bank -> `assets/python-scripts/script_073_interview_question_bank.py`
- 074. Mock Interview Scoring -> `assets/python-scripts/script_074_mock_interview_scoring.py`
- 075. Portfolio Project Tracker -> `assets/python-scripts/script_075_portfolio_project_tracker.py`
- 076. Certification Tracker -> `assets/python-scripts/script_076_certification_tracker.py`
- 077. Study Schedule Generator -> `assets/python-scripts/script_077_study_schedule_generator.py`
- 078. Job Application Tracker -> `assets/python-scripts/script_078_job_application_tracker.py`
- 079. Salary Comparison Tool -> `assets/python-scripts/script_079_salary_comparison_tool.py`
- 080. LinkedIn Keyword Optimizer -> `assets/python-scripts/script_080_linkedin_keyword_optimizer.py`
- 081. Load Curve Plotter -> `assets/python-scripts/script_081_load_curve_plotter.py`
- 082. Voltage Trend Analyzer -> `assets/python-scripts/script_082_voltage_trend_analyzer.py`
- 083. Harmonic Bar Chart -> `assets/python-scripts/script_083_harmonic_bar_chart.py`
- 084. Anomaly Detection (Simple) -> `assets/python-scripts/script_084_anomaly_detection_simple.py`
- 085. Power Quality Dashboard (Basic) -> `assets/python-scripts/script_085_power_quality_dashboard_basic.py`
- 086. Correlation Matrix -> `assets/python-scripts/script_086_correlation_matrix.py`
- 087. Missing Data Filler -> `assets/python-scripts/script_087_missing_data_filler.py`
- 088. Substation Monitoring Plot -> `assets/python-scripts/script_088_substation_monitoring_plot.py`
- 089. Energy Consumption Breakdown -> `assets/python-scripts/script_089_energy_consumption_breakdown.py`
- 090. Real-Time Data Simulator -> `assets/python-scripts/script_090_real_time_data_simulator.py`
- 091. Transmission Loss Optimization -> `assets/python-scripts/script_091_transmission_loss_optimization.py`
- 092. Economic Load Dispatch (Simple) -> `assets/python-scripts/script_092_economic_load_dispatch_simple.py`
- 093. Capacitor Placement Optimizer -> `assets/python-scripts/script_093_capacitor_placement_optimizer.py`
- 094. Battery Dispatch Optimizer -> `assets/python-scripts/script_094_battery_dispatch_optimizer.py`
- 095. Renewable Mix Optimization -> `assets/python-scripts/script_095_renewable_mix_optimization.py`
- 096. Transformer Load Balancing -> `assets/python-scripts/script_096_transformer_load_balancing.py`
- 097. Voltage Setpoint Optimization -> `assets/python-scripts/script_097_voltage_setpoint_optimization.py`
- 098. Multi-Criteria Decision Model -> `assets/python-scripts/script_098_multi_criteria_decision_model.py`
- 099. Maintenance Scheduling -> `assets/python-scripts/script_099_maintenance_scheduling.py`
- 100. Engineering Decision Support System -> `assets/python-scripts/script_100_engineering_decision_support_system.py`
