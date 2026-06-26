import sys
import pandas as pd

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide a CSV path.")
        return
    
    csv_path = sys.argv[1]
    try:
        df = pd.read_csv(csv_path)
        
        print(f"✅ **CSV Analysis Complete**")
        print(f"📊 Rows: {len(df)}")
        print(f"📋 Columns: {list(df.columns)}")
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            print("\n📈 Numeric Column Stats:")
            for col in numeric_cols:
                print(f"   • {col}: Avg = {df[col].mean():.2f} | Min = {df[col].min()} | Max = {df[col].max()}")
        else:
            print("\nNo numeric columns found.")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()