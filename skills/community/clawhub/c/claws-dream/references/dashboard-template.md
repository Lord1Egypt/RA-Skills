# Memory Dashboard Template

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Memory Dashboard</title>
  <style>
    body { font-family: system-ui; max-width: 800px; margin: 40px auto; padding: 20px; background: #0f0f1a; color: #e0e0e0; }
    h1 { color: #7dd3fc; }
    .card { background: #1a1a2e; border-radius: 12px; padding: 20px; margin: 16px 0; }
    .score { font-size: 48px; font-weight: bold; }
    .excellent { color: #4ade80; }
    .good { color: #a3e635; }
    .fair { color: #facc15; }
    .poor { color: #f87171; }
    .critical { color: #ef4444; }
    .metrics { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-top: 16px; }
    .metric { background: #252540; padding: 12px; border-radius: 8px; text-align: center; }
    .metric-value { font-size: 24px; font-weight: bold; }
    .metric-label { font-size: 11px; color: #888; margin-top: 4px; }
    .streak { color: #c084fc; }
    .entries { color: #7dd3fc; }
    .footer { text-align: center; color: #666; margin-top: 40px; font-size: 12px; }
  </style>
</head>
<body>
  <h1>🧠 Memory Dashboard</h1>
  
  <div class="card">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <div>
        <div class="label">Health Score</div>
        <div class="score [[HEALTH_CLASS]]">[[HEALTH_SCORE]]</div>
      </div>
      <div style="text-align: right;">
        <div class="streak">🔥 Streak: [[STREAK]] dreams</div>
        <div class="entries">📊 [[TOTAL_ENTRIES]] entries</div>
      </div>
    </div>
    
    <div class="metrics">
      <div class="metric">
        <div class="metric-value">[[FRESHNESS]]%</div>
        <div class="metric-label">Freshness</div>
      </div>
      <div class="metric">
        <div class="metric-value">[[COVERAGE]]%</div>
        <div class="metric-label">Coverage</div>
      </div>
      <div class="metric">
        <div class="metric-value">[[COHERENCE]]%</div>
        <div class="metric-label">Coherence</div>
      </div>
      <div class="metric">
        <div class="metric-value">[[EFFICIENCY]]%</div>
        <div class="metric-label">Efficiency</div>
      </div>
      <div class="metric">
        <div class="metric-value">[[REACHABILITY]]%</div>
        <div class="metric-label">Reachability</div>
      </div>
    </div>
  </div>
  
  <div class="card">
    <h3>📈 Health History</h3>
    [[HEALTH_CHART]]
  </div>
  
  <div class="card">
    <h3>🌊 Open Threads</h3>
    [[OPEN_THREADS]]
  </div>
  
  <div class="footer">
    Last dream: [[LAST_DREAM]] · Powered by Nightly Dream
  </div>
</body>
</html>
```
