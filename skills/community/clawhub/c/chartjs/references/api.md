# Chart.js API Reference

## Table of Contents

- [Data Structure](#data-structure)
- [Axes](#axes)
- [Colors & Styling](#colors--styling)
- [Animation](#animation)
- [Plugins](#plugins)

---

## Data Structure

### Basic Structure
```javascript
{
  type: 'bar',           // Chart type
  data: {
    labels: [],          // X-axis labels
    datasets: [{
      label: '',         // Dataset name
      data: [],          // Data array
      // ...style properties
    }]
  },
  options: {}            // Configuration
}
```

### Data Formats

**Line/Bar Charts:**
```javascript
data: [12, 19, 3, 5, 2, 3]  // Numeric array
```

**Scatter Chart (x, y):**
```javascript
data: [{ x: 10, y: 20 }, { x: 15, y: 10 }]
```

**Bubble Chart (x, y, r):**
```javascript
data: [{ x: 10, y: 20, r: 5 }]
```

---

## Axes

### Cartesian Scales (x/y)

**CategoryScale (default x-axis):**
```javascript
scales: {
  x: { type: 'category', labels: ['January','February','March'] }
}
```

**LinearScale (default y-axis):**
```javascript
scales: {
  y: {
    type: 'linear',
    beginAtZero: true,
    min: 0,
    max: 100,
    ticks: { stepSize: 10 }
  }
}
```

**LogarithmicScale:**
```javascript
scales: {
  y: { type: 'logarithmic' }
}
```

**TimeScale:**
```javascript
scales: {
  x: {
    type: 'time',
    time: { unit: 'day', displayFormat: 'MMM D' }
  }
}
```

### Radial Scales (Radar/Polar Area)

**RadialLinearScale:**
```javascript
scales: {
  r: {
    angleLines: { display: true },
    ticks: { display: false },
    pointLabels: { font: { size: 14 } }
  }
}
```

### Tick Configuration
```javascript
ticks: {
  color: '#666',
  font: { size: 12, family: 'Arial' },
  callback: (value) => value + 'k',  // Format display value
  maxTicksLimit: 10
}
```

### Axis Titles
```javascript
scales: {
  x: {
    title: { display: true, text: 'Month', color: '#333' }
  },
  y: {
    title: { display: true, text: 'Sales (10k)', color: '#333' }
  }
}
```

---

## Colors & Styling

### Dataset Styles
```javascript
datasets: [{
  // Fill color
  backgroundColor: 'rgba(54, 162, 235, 0.5)',
  // Border color
  borderColor: 'rgb(54, 162, 235)',
  // Border width
  borderWidth: 2,
  // Hover color
  hoverBackgroundColor: 'rgba(54, 162, 235, 1)',
  // Hover border color
  hoverBorderColor: '#fff',
  // Point radius (line chart)
  pointRadius: 4,
  // Point hover radius
  pointHoverRadius: 6,
  // Point style: 'circle','rect','rectRot','cross','crossRot','star','line','dash'
  pointStyle: 'circle',
}]
```

### Gradients
```javascript
const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(255, 99, 132, 0.5)');
gradient.addColorStop(1, 'rgba(255, 99, 132, 0)');
data: { datasets: [{ backgroundColor: gradient }] }
```

### Border Radius (Bar)
```javascript
datasets: [{
  borderRadius: 5,           // All corners
  borderSkipped: false,      // or 'left'/'right'/'top'/'bottom'
}]
```

### Grid Background
```javascript
options: {
  scales: {
    x: { grid: { display: false } },
    y: { grid: { color: '#eee' } }
  }
}
```

---

## Animation

### Global Animation Configuration
```javascript
options: {
  animation: {
    duration: 1000,        // Animation duration ms
    easing: 'easeOutQuart'  // Easing function
  }
}
```

### Easing Function Options
`'linear'` | `'easeInQuad'` | `'easeOutQuad'` | `'easeInOutQuad'` | `'easeInCubic'` | `'easeOutCubic'` | `'easeInOutCubic'` | `'easeInQuart'` | `'easeOutQuart'` | `'easeInOutQuart'` | `'easeInQuint'` | `'easeOutQuint'` | `'easeInOutQuint'` | `'easeInSine'` | `'easeOutSine'` | `'easeInOutSine'` | `'easeInExpo'` | `'easeOutExpo'` | `'easeInOutExpo'` | `'easeInCirc'` | `'easeOutCirc'` | `'easeInOutCirc'` | `'easeInElastic'` | `'easeOutElastic'` | `'easeInOutElastic'` | `'easeInBack'` | `'easeOutBack'` | `'easeInOutBack'` | `'easeInBounce'` | `'easeOutBounce'` | `'easeInOutBounce'`

### Disable Animation
```javascript
animation: false
// or
animation: { duration: 0 }
```

### Delayed Loading
```javascript
animation: {
  delay: (context) => context.dataIndex * 100  // Delay each data point sequentially
}
```

---

## Plugins

### Built-in Plugins (Register as needed)
```javascript
import {
  Chart,
  BarController, BarElement,
  LineController, LineElement, PointElement,
  PieController, ArcElement,
  CategoryScale, LinearScale,
  Tooltip, Legend, Filler
} from 'chart.js';

Chart.register(
  BarController, BarElement,
  LineController, LineElement, PointElement,
  PieController, ArcElement,
  CategoryScale, LinearScale,
  Tooltip, Legend, Filler
);
```

### Plugin List

| Plugin | Purpose |
|-----|------|
| Decimation | Data decimation, reduces points |
| Filler | Fill line chart area |
| Legend | Legend display |
| SubTitle | Subtitle |
| Title | Title |
| Tooltip | Hover tooltip |

### Title Configuration
```javascript
options: {
  plugins: {
    title: {
      display: true,
      text: 'Monthly Sales Report',
      color: '#333',
      font: { size: 18, weight: 'bold' },
      padding: { top: 10, bottom: 30 }
    }
  }
}
```

### Legend Configuration
```javascript
options: {
  plugins: {
    legend: {
      display: true,
      position: 'top',        // 'top'/'bottom'/'left'/'right'
      labels: {
        color: '#333',
        font: { size: 14 },
        usePointStyle: true    // Use points instead of color blocks
      }
    }
  }
}
```

### Tooltip Configuration
```javascript
options: {
  plugins: {
    tooltip: {
      enabled: true,
      mode: 'index',          // 'point'/'nearest'/'dataset'/'index'
      intersect: false,
      callbacks: {
        label: (context) => `${context.dataset.label}: ${context.raw}`
      }
    }
  }
}
```

---

## Complete Example

### Gradient Filled Line Chart
```javascript
const ctx = document.getElementById('myChart').getContext('2d');
const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(75, 192, 192, 0.4)');
gradient.addColorStop(1, 'rgba(75, 192, 192, 0)');

new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['January', 'February', 'March', 'April', 'May'],
    datasets: [{
      label: 'User Growth',
      data: [30, 45, 62, 78, 95],
      fill: true,
      backgroundColor: gradient,
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.4
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: true },
      tooltip: { mode: 'index', intersect: false }
    },
    scales: {
      y: { beginAtZero: false }
    }
  }
});
```