# Pivot + AINav Recipes

## Recipe 1: Controlled pivot table with hook

```tsx
import { CPivotTable, usePivotTable } from 'orbcafe-ui';

const pivot = usePivotTable({
  fields,
  initialLayout: {
    rows: ['region'],
    columns: ['quarter'],
    values: [{ fieldId: 'revenue', aggregation: 'sum' }],
  },
});

<CPivotTable rows={dataRows} fields={fields} model={pivot.model} />;
```

## Recipe 2: Pivot preset management

```tsx
import { CPivotTable, type PivotTablePreset } from 'orbcafe-ui';

const [presets, setPresets] = useState<PivotTablePreset[]>([]);

<CPivotTable
  rows={rows}
  fields={fields}
  enablePresetManagement
  presets={presets}
  onPresetsChange={setPresets}
/>;
```

## Recipe 3: Controlled pivot with PivotChart defaults

```tsx
import { CPivotTable, usePivotTable } from 'orbcafe-ui';

const pivot = usePivotTable({
  fields,
  initialLayout: {
    rows: ['region'],
    columns: ['quarter'],
    values: [
      { fieldId: 'revenue', aggregation: 'sum' },
      { fieldId: 'profit', aggregation: 'sum' },
    ],
  },
  initialChart: {
    dimensionFieldId: 'quarter',
    primaryValueFieldId: 'revenue',
    secondaryValueFieldId: 'profit',
    chartType: 'bar-vertical',
  },
});

<CPivotTable rows={rows} fields={fields} model={pivot.model} />;
```

要点：

- 默认图表维度优先取 `rows[0]`，否则 `columns[0]`
- 图表最多只展示 1 个维度、2 个度量
- 多维或多度量时显示 4 个下拉，且应保持等宽

## Recipe 4: Voice navigation provider

```tsx
import { CAINavProvider } from 'orbcafe-ui';

<CAINavProvider
  onVoiceSubmit={async (text) => {
    await routeByIntent(text);
  }}
  onVoiceError={(err) => console.error(err)}
  longPressMs={200}
  wsUrl="ws://localhost:8765"
>
  {children}
</CAINavProvider>;
```
