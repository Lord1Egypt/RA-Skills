#!/usr/bin/env python3
"""
Financial Analytics Pro - Core Analysis Module
Premium financial analysis tool for business intelligence
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import sys
import argparse
from pathlib import Path

class FinancialAnalyzer:
    """Core financial analysis engine for Financial Analytics Pro"""
    
    def __init__(self):
        self.data = None
        self.results = {}
        
    def load_data(self, filepath):
        """Load financial data from CSV or Excel file"""
        try:
            if filepath.endswith('.csv'):
                self.data = pd.read_csv(filepath)
            elif filepath.endswith('.xlsx') or filepath.endswith('.xls'):
                self.data = pd.read_excel(filepath)
            else:
                raise ValueError("Unsupported file format. Use CSV or Excel.")
            
            print(f"✓ Loaded {len(self.data)} records from {filepath}")
            return True
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return False
    
    def analyze_income_statement(self):
        """Analyze income statement data"""
        if self.data is None:
            return None
            
        analysis = {
            'total_revenue': self.data.get('Revenue', pd.Series([0])).sum(),
            'total_expenses': self.data.get('Expenses', pd.Series([0])).sum(),
            'net_income': 0,
            'gross_margin': 0,
            'net_margin': 0
        }
        
        # Calculate net income
        analysis['net_income'] = analysis['total_revenue'] - analysis['total_expenses']
        
        # Calculate margins
        if analysis['total_revenue'] > 0:
            analysis['gross_margin'] = (analysis['net_income'] / analysis['total_revenue']) * 100
            analysis['net_margin'] = (analysis['net_income'] / analysis['total_revenue']) * 100
        
        # Monthly trends if date column exists
        if 'Date' in self.data.columns:
            self.data['Date'] = pd.to_datetime(self.data['Date'])
            monthly = self.data.groupby(self.data['Date'].dt.to_period('M')).agg({
                'Revenue': 'sum',
                'Expenses': 'sum'
            }).reset_index()
            monthly['Profit'] = monthly['Revenue'] - monthly['Expenses']
            analysis['monthly_trends'] = monthly.to_dict('records')
        
        self.results['income_statement'] = analysis
        return analysis
    
    def calculate_financial_ratios(self):
        """Calculate key financial ratios"""
        if self.data is None:
            return None
            
        ratios = {}
        
        # Get required columns with defaults
        revenue = self.data.get('Revenue', pd.Series([0])).sum()
        expenses = self.data.get('Expenses', pd.Series([0])).sum()
        assets = self.data.get('Assets', pd.Series([0])).sum()
        liabilities = self.data.get('Liabilities', pd.Series([0])).sum()
        equity = self.data.get('Equity', pd.Series([0])).sum()
        
        # Profitability ratios
        if revenue > 0:
            ratios['gross_profit_margin'] = ((revenue - expenses) / revenue) * 100
            ratios['net_profit_margin'] = ((revenue - expenses) / revenue) * 100
            ratios['return_on_assets'] = ((revenue - expenses) / assets) * 100 if assets > 0 else 0
            ratios['return_on_equity'] = ((revenue - expenses) / equity) * 100 if equity > 0 else 0
        
        # Liquidity ratios
        current_assets = self.data.get('Current_Assets', pd.Series([0])).sum()
        current_liabilities = self.data.get('Current_Liabilities', pd.Series([0])).sum()
        
        if current_liabilities > 0:
            ratios['current_ratio'] = current_assets / current_liabilities
        if current_liabilities > 0:
            # Quick ratio (assuming inventory is part of current assets)
            inventory = self.data.get('Inventory', pd.Series([0])).sum()
            ratios['quick_ratio'] = (current_assets - inventory) / current_liabilities
        
        # Solvency ratios
        if equity > 0:
            ratios['debt_to_equity'] = liabilities / equity
        
        self.results['financial_ratios'] = ratios
        return ratios
    
    def generate_forecast(self, periods=12):
        """Generate simple financial forecast"""
        if self.data is None or 'Revenue' not in self.data.columns:
            return None
            
        # Simple moving average forecast
        revenue_series = self.data['Revenue'].dropna()
        if len(revenue_series) < 2:
            return None
            
        # Calculate growth rate (simple average)
        growth_rates = revenue_series.pct_change().dropna()
        avg_growth = growth_rates.mean() if len(growth_rates) > 0 else 0.05  # Default 5%
        
        # Generate forecast
        last_revenue = revenue_series.iloc[-1]
        forecast = []
        
        for i in range(1, periods + 1):
            forecast_revenue = last_revenue * (1 + avg_growth) ** i
            forecast_expenses = forecast_revenue * 0.7  # Assume 70% expense ratio
            forecast_profit = forecast_revenue - forecast_expenses
            
            forecast.append({
                'period': i,
                'revenue': round(forecast_revenue, 2),
                'expenses': round(forecast_expenses, 2),
                'profit': round(forecast_profit, 2)
            })
        
        self.results['forecast'] = forecast
        return forecast
    
    def create_report(self, output_file=None):
        """Generate comprehensive financial report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'analysis': self.results,
            'summary': self._generate_summary()
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"✓ Report saved to {output_file}")
        
        return report
    
    def _generate_summary(self):
        """Generate executive summary"""
        summary = []
        
        if 'income_statement' in self.results:
            is_data = self.results['income_statement']
            summary.append(f"Total Revenue: ${is_data['total_revenue']:,.2f}")
            summary.append(f"Total Expenses: ${is_data['total_expenses']:,.2f}")
            summary.append(f"Net Income: ${is_data['net_income']:,.2f}")
            summary.append(f"Net Margin: {is_data['net_margin']:.1f}%")
        
        if 'financial_ratios' in self.results:
            ratios = self.results['financial_ratios']
            if 'current_ratio' in ratios:
                summary.append(f"Current Ratio: {ratios['current_ratio']:.2f}")
            if 'debt_to_equity' in ratios:
                summary.append(f"Debt to Equity: {ratios['debt_to_equity']:.2f}")
        
        return summary
    
    def visualize(self, output_dir='.'):
        """Create financial visualizations"""
        if self.data is None:
            return False
            
        try:
            # Set style
            plt.style.use('seaborn-v0_8-darkgrid')
            
            # Revenue vs Expenses chart
            if 'Revenue' in self.data.columns and 'Expenses' in self.data.columns:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # If we have dates, use them
                if 'Date' in self.data.columns:
                    dates = pd.to_datetime(self.data['Date'])
                    ax.plot(dates, self.data['Revenue'], label='Revenue', marker='o', linewidth=2)
                    ax.plot(dates, self.data['Expenses'], label='Expenses', marker='s', linewidth=2)
                    ax.set_xlabel('Date')
                    plt.xticks(rotation=45)
                else:
                    ax.plot(self.data['Revenue'].values, label='Revenue', marker='o', linewidth=2)
                    ax.plot(self.data['Expenses'].values, label='Expenses', marker='s', linewidth=2)
                    ax.set_xlabel('Period')
                
                ax.set_ylabel('Amount ($)')
                ax.set_title('Revenue vs Expenses Over Time')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                plt.tight_layout()
                plt.savefig(f'{output_dir}/revenue_vs_expenses.png', dpi=150)
                plt.close()
                print(f"✓ Saved visualization: {output_dir}/revenue_vs_expenses.png")
            
            return True
            
        except Exception as e:
            print(f"✗ Error creating visualization: {e}")
            return False

def main():
    """Command-line interface for Financial Analytics Pro"""
    parser = argparse.ArgumentParser(description='Financial Analytics Pro - Premium Financial Analysis Tool')
    parser.add_argument('file', help='Financial data file (CSV or Excel)')
    parser.add_argument('--analyze', action='store_true', help='Run full financial analysis')
    parser.add_argument('--ratios', action='store_true', help='Calculate financial ratios')
    parser.add_argument('--forecast', type=int, help='Generate forecast for N periods')
    parser.add_argument('--report', help='Output report file (JSON)')
    parser.add_argument('--visualize', action='store_true', help='Create visualizations')
    parser.add_argument('--output-dir', default='.', help='Output directory for files')
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = FinancialAnalyzer()
    
    # Load data
    if not analyzer.load_data(args.file):
        sys.exit(1)
    
    # Run analyses based on arguments
    if args.analyze:
        print("\n" + "="*60)
        print("FINANCIAL ANALYSIS REPORT")
        print("="*60)
        
        # Income statement analysis
        income = analyzer.analyze_income_statement()
        if income:
            print("\n📊 INCOME STATEMENT ANALYSIS:")
            print(f"  Total Revenue: ${income['total_revenue']:,.2f}")
            print(f"  Total Expenses: ${income['total_expenses']:,.2f}")
            print(f"  Net Income: ${income['net_income']:,.2f}")
            print(f"  Net Margin: {income['net_margin']:.1f}%")
    
    if args.ratios:
        ratios = analyzer.calculate_financial_ratios()
        if ratios:
            print("\n📈 FINANCIAL RATIOS:")
            for ratio, value in ratios.items():
                print(f"  {ratio.replace('_', ' ').title()}: {value:.2f}")
    
    if args.forecast:
        forecast = analyzer.generate_forecast(args.forecast)
        if forecast:
            print(f"\n🔮 {args.forecast}-PERIOD FORECAST:")
            for period in forecast[:3]:  # Show first 3 periods
                print(f"  Period {period['period']}: Revenue=${period['revenue']:,.0f}, Profit=${period['profit']:,.0f}")
            if len(forecast) > 3:
                print(f"  ... and {len(forecast)-3} more periods")
    
    if args.visualize:
        if analyzer.visualize(args.output_dir):
            print("\n🎨 Visualizations created successfully")
    
    if args.report:
        report = analyzer.create_report(args.report)
        if report:
            print(f"\n📄 Report generated: {args.report}")
    
    print("\n" + "="*60)
    print("Financial Analytics Pro - Analysis Complete")
    print("="*60)

if __name__ == "__main__":
    main()