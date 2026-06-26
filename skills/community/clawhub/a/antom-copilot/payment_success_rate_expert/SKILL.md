---
name: payment_success_rate_expert
description: "Antom Payment Success Rate Expert - Focused on payment success rate data pulling, analysis, report generation, and sending"
metadata:
  {
    "copaw":
      {
        "emoji": "📊",
        "requires": {}
      }
  }
---

# Payment Success Rate Expert
Hello! I am the Antom Payment Success Rate Expert, focusing on payment success rate data processing and reporting.

## 🔧 Prerequisites and Configuration Requirements

### System Requirements
- **Operating System**: macOS, Linux, or Windows
- **Python Version**: Python 3.6+

### Python Dependencies

#### Capability One: query_antom_psr_data.py
```bash
pip install requests
```

#### Capability Two: analyse_and_gen_report.py
```bash
pip install matplotlib reportlab numpy
```

#### Capability Three: send_psr_report.py
- Uses only Python standard library, no additional installation required

### Configuration File Requirements

**Configuration File Location**: `~/antom/conf.json`

**Configuration File Format**:
```json
{
  "merchant_token": "Your Merchant Token",
  "email_conf": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your-email@gmail.com",
    "password": "your-app-password",
    "use_tls": true
  }
}
```

**Configuration Parameter Description**:
- `merchant_token`: Merchant Token (required, for API authentication)
- `email_conf`: Email configuration (required for capability three)
  - `smtp_server`: SMTP server address
  - `smtp_port`: SMTP port number (usually 587)
  - `username`: Sender email address
  - `password`: Email password or app-specific password
  - `use_tls`: Whether to use TLS encryption (default: true)

### Directory Structure Requirements

Scripts will automatically create the following directory structure:
```
~/antom/
├── conf.json                # Configuration file
└── success rate/            # Data storage directory
    ├── 20260323_raw_data.json              # Raw data file (output of capability one)
    └── 20260323/                           # Report directory (created by capability two)
        ├── 20260323-Payment-Success-Rate-Report-{merchant_id}.pdf  # PDF report (output of capability two)
        ├── 20260323_executive_summary.txt   # Executive summary (output of capability two)
        └── images/                          # Charts directory (created by capability two)
            ├── card_overall.png
            ├── card_error_pie.png
            ├── apm_overall.png
            └── apm_error_pie.png
```

### API Endpoint

**query_antom_psr_data.py** uses the following API endpoint:
- **URL**: `https://ibotservice.alipayplus.com/almpapi/v1/message/chat`
- **Method**: POST
- **Authentication**: Uses merchant_id and merchant_token from configuration
- **Request Format**: JSON
- **Timeout Setting**: 30 seconds

### Execution Order Dependencies

**Normal Workflow**:
1. **Step One**: Run `query_antom_psr_data.py` to pull data
   - Input: Target date (e.g., 20260325)
   - **T+1 Logic**: Only when querying "today", use yesterday's data (since today's data is not yet generated)
   - Output: `~/antom/success rate/{date}_raw_data.json` (7 files total)
   
2. **Step Two**: Run `analyse_and_gen_report.py` to generate report
   - Input: Target date (e.g., 20260325)
   - **T+1 Logic**: Only when querying "today", analyze yesterday's data
   - Dependency: Raw data files generated in step one
   - Output: PDF report, executive summary, and charts
   
3. **Step Three**: Run `send_psr_report.py` to send report
   - Input: Target date and recipient email
   - **T+1 Logic**: Only when sending "today's" report, use yesterday's report
   - Dependency: PDF report and executive summary generated in step two
   - Output: Email sent

**Note**: The three capabilities must be executed in sequence. Subsequent capabilities depend on the output files from the previous step.

**Important Note - T+1 Data Generation Logic**:
Since Antom data is generated on a T+1 basis (today's data can only be retrieved the next day), the script automatically handles this logic:
- When user queries "today" (e.g., 20260325): Automatically uses yesterday's data (20260324)
- When user queries a historical date (e.g., 20260320): Directly uses that date's data (20260320)
- This is implemented through the internal `calculate_t1_date()` function
- Users don't need to manually calculate dates, just provide the date you want to query

## 📋 Capability List

### Capability One: Pull Merchant Payment Success Rate Data
- Pull payment success rate data from Antom server
- Available script: `query_antom_psr_data.py`
- Accepts parameter: Date range (format: YYYYMMDD~YYYYMMDD)
- Prerequisite: Configuration file must contain valid merchant_token
- Output file: `~/antom/success rate/{start_date}_raw_data.json`

### Capability Two: Analyze Data and Generate PDF Report
- Analyze merchant payment success rate data
- Generate PDF analysis report with charts and executive summary
- Available script: `analyse_and_gen_report.py`
- Accepts parameter: Date (format: YYYYMMDD)
- Prerequisites:
  - Capability one has been executed and raw data files generated
- Output files:
  - PDF report: `~/antom/success rate/{date}/{date}-Payment-Success-Rate-Report.pdf`
  - Executive summary: `~/antom/success rate/{date}/{date}_executive_summary.txt`
  - Chart files: Stored in `~/antom/success rate/{date}/images/` directory

### Capability Three: Send Payment Success Rate Report
- Send the generated report to specified recipients
- Available script: `send_psr_report.py`
- Accepts parameters:
  - Parameter one: Date (format: YYYYMMDD)
  - Parameter two: Recipient email address
- Prerequisites:
  - Capability two has been executed and PDF report generated
  - Configuration file must contain complete email_conf
- Features:
  - Automatically analyzes data and generates intelligent risk insights
  - Supports attachment sending (PDF report)
  - Includes executive summary in email body

## 💡 Usage Examples

### Complete Workflow Example

**Example 1: Generate Today's Report (Using T+1 Logic)**
```bash
# Step One: Pull yesterday's data (automatically applies T+1 logic)
# Assuming today is 20260325, will actually query 20260324 and the previous week
python query_antom_psr_data.py --date 20260325

# Step Two: Generate yesterday's report
python analyse_and_gen_report.py --date 20260325

# Step Three: Send report
python send_psr_report.py --date 20260325 --recipient merchant@example.com
```

**Important Note**: 
- Users don't need to worry about T+1 details, just provide the date you want to report
- Scripts automatically adjust the date (actual date = user specified date - 1 day)
- Analysis reports and emails will display the user-specified target date

**Simplified Command (Using Automation Script)**:
```bash
# One-click generate and send today's report (actually yesterday's data)
./generate_today_report.sh merchant@example.com
```

## ⚠️ Common Issues

1. **Configuration File Not Found Error**
   - Ensure `~/antom/conf.json` has been created
   - Check if configuration file format is correct (valid JSON)

2. **Missing Dependency Package Error**
   - Install corresponding Python packages based on capability requirements
   - Use `pip install -r requirements.txt` for batch installation

3. **File Not Found Error**
   - Ensure scripts are executed in sequence
   - Check if previous step completed successfully and generated output files

4. **Email Sending Failure**
   - Check if email_conf configuration is correct
   - Confirm SMTP server address and port
   - Verify email account and password (app-specific password recommended)

## ✨ Enhanced Features (v2.0)

### Automatic Data Recovery
- **Smart Date Selection**: When target date has no data, automatically searches backwards up to 7 days to find the most recent valid data
- **Graceful Degradation**: If no data is found for a specific payment method (Card or APM), the report will skip that section without failing
- **Enhanced Validation**: Improved data validity checking that accepts either Card or APM data (instead of requiring both)

### Robust Data Handling
- **Missing Field Tolerance**: Automatically handles missing data fields (e.g., 3DS authentication data) without crashing
- **Section-Based Generation**: Only generates report sections for which data is available
- **Detailed Diagnostics**: Provides clear console output showing what data was found and what sections will be generated

### Error Prevention
- **Pre-Flight Checks**: Validates data existence and content before attempting report generation
- **Informative Messages**: Clear error messages with actionable steps when issues are detected
- **Graceful Failures**: Continues report generation even when some metrics are unavailable

### Smart Display Logic (v2.1)
- **Conditional Auth Display**: Only displays 3DS and Non-3DS authentication rates when the data actually exists, preventing misleading 0% displays
- **Adaptive Executive Summary**: Executive summary dynamically adjusts to show only available authentication methods
- **Data Quality Filtering**: Automatically filters out low-quality or unknown data types (e.g., 'unknown' authentication category) from analysis

**Bug Fix (v2.1)**: Fixed issue where missing 3DS data would display as "3DS Success Rate: 0.0%" in analysis summaries, which was misleading. Now only displays rates for authentication methods that actually have data.

### Chart Display Improvement (v2.1)
- **Fixed Y-Axis Range**: Success rate charts now use a fixed 0-100% y-axis range, ensuring consistent visualization
- **Clear Rate Indication**: Prevents misinterpretation when success rates are high (e.g., 83% no longer appears near the bottom of the chart)
- **Better Visual Comparison**: Makes it easy to quickly assess performance at a glance

**Bug Fix (v2.1)**: Fixed visual issue where success rate line charts could appear to show ~0% when the actual rate was high (e.g., 83%). This was caused by matplotlib's auto-scaling when all data points had similar values. Charts now explicitly use 0-100% y-axis range.

### Enhanced Analysis Sections (v2.2)

#### Dynamic Section Numbering
- **Independent Counters**: Card and APM sections now use separate counters (`card_section_counter` and `apm_section_counter`)
- **Automatic Numbering**: Sections are numbered dynamically based on available data, preventing numbering gaps when sections are skipped
- **Clean Layout**: Ensures consistent numbering whether error data or optional sections are present

**Feature Enhancement (v2.2)**: Implemented dynamic section numbering to handle conditional sections gracefully.

#### Country & Bank Analysis Enhancement
- **Top 10 by Improvement**: Displays top 10 countries and banks sorted by **success rate change** (today vs yesterday), highlighting biggest improvements
- **Bottom 10 by Decline**: Shows bottom 10 countries and banks by success rate change, filtering by minimum transaction threshold (5 for banks, countries also have volume threshold)
- **Action-Oriented Sorting**: Both top and bottom performers are ordered by change magnitude rather than volume, making it easy to identify what improved and what needs attention
- **Smart Analysis Summary**: When bank count exceeds 20, analysis summary only examines Top 10 and Bottom 10 banks (filtering low performers), preventing information overload while maintaining actionable insights
- **Comprehensive Coverage**: Country analysis now matches bank analysis in depth and presentation style

**Feature Enhancement (v2.2)**: Country and bank analysis now focus on change detection rather than static rankings, providing more actionable insights for merchant optimization. Merchants can quickly identify:
- Which countries/banks' performance is improving most (top 10 by change)
- Which countries/banks' performance is declining (bottom 10 by change)

#### APM Terminal Analysis Addition
- **Terminal Type Breakdown**: New section analyzing APM performance by terminal type (e.g., APP, WEB, WAP)
- **Volume and Rate Tracking**: Shows success rates, transaction volumes, and changes vs. previous periods
- **Baseline Data Handling**: Missing yesterday/week data are handled intelligently (yesterday defaults to 0%, week avg equals today's rate when only one day available)
- **Actionable Insights**: Automatically highlights underperforming terminal types with specific recommendations

**Feature Addition (v2.2)**: Added comprehensive terminal analysis for APM payments, enabling merchants to identify and optimize performance issues across different channels (mobile app, web, mobile web).

#### Historical Data Handling (v2.2)
- **Yesterday Baseline**: When previous day data is unavailable, defaults to 0% (showing improvement from zero baseline)
- **Week Average Logic**: When only one day of data exists, week average equals today's rate (resulting in zero weekly change, which is statistically correct)
- **Clear Visual Indicators**: Table clearly shows when baseline data is missing vs. when actual historical data exists

**Bug Fix (v2.2)**: Fixed terminal analysis to properly handle missing historical data. Yesterday now defaults to 0% and week average defaults to today's rate when only one day of data is available, preventing misleading change calculations.

#### Executive Summary Risk Classification (v2.2)
- **Volume Change Categorization**: Significant volume changes are now properly categorized based on direction
  - **Increases >50%**: Classified as "Significant volume increase" in POSITIVE PERFORMANCE
  - **Declines <-50%**: Classified as "⚠️ Significant volume decline" in KEY RISKS AND CONCERNS
- **Authentication Performance Context**: Authentication method descriptions now include performance context
  - **Success rate ≥80%**: "strong performance" or "performing well"
  - **Success rate 70-80%**: "acceptable"
  - **Success rate <70%**: "⚠️ needs improvement" (moved to WARNINGS)
- **Accurate Risk Representation**: Volume declines and underperforming authentication methods are no longer misrepresented as positive observations

**Bug Fix (v2.2)**: Fixed executive summary to properly categorize volume declines as risks and provide context for authentication performance ratings. Previously, both increases and declines >50% were placed in POSITIVE PERFORMANCE section, and authentication methods lacked performance context.

This ensures the report generation is resilient to data gaps and provides maximum value even when some data sources are unavailable.

## 📞 Technical Support

For any issues, please contact Antom technical support or visit: https://global.alipay.com

---

This skill is automatically called by the antom_copilot main skill based on user intent, primarily handling queries and operations related to payment success rate.

### v2.3 (Current) - Enhanced Compatibility & Robustness
- **Week Data Validation**: Sections automatically hide if week data is completely empty (no historical context)
- **Zero-Fill for Missing Data**: When today has no transactions but historical data exists, displays 0 for today while preserving week average calculations
- **Smart Display Logic**: 
  - Country/Bank analysis shows **all entries** when ≤20 total
  - Shows **Top 10 + Bottom 10** when >20 total (maintains performance)
- **Display Consistency**: Country analysis now matches bank analysis logic

**Compatibility Enhancement (v2.3)**: The report generation is now more resilient to data gaps:
- Sections won't display if there's no week data (avoiding empty/meaningless sections)
- Historical data can still be shown even when today has no transactions
- Prevents information overload while maintaining depth when needed
