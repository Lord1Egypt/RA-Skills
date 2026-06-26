# Token and Components

## Suggested theme token baseline

```ts
export const adminTheme = {
  token: {
    colorPrimary: '#1677FF',
    colorSuccess: '#00CA75',
    colorWarning: '#FF8008',
    colorError: '#FF525C',
    colorText: '#333333',
    colorTextSecondary: '#545759',
    colorTextTertiary: '#8C8C8C',
    colorBorder: '#EBECED',
    colorBgLayout: '#F5F7FA',
    colorBgContainer: '#FFFFFF',
    borderRadius: 6,
    borderRadiusLG: 10,
    borderRadiusSM: 4,
    fontSize: 14,
    fontFamily: 'PingFang SC, Segoe UI, Helvetica Neue, Arial, sans-serif'
  }
}
```

## Alias token suggestions

```ts
export const adminAliasTokens = {
  brandPrimary: '#1677FF',
  brandGradientStart: '#2586FF',
  brandGradientEnd: '#2874FC',
  colorNavBg: '#292E33',
  colorPageBgSoft: '#EBF2FF',
  colorHintBg: '#F2FAFF',
  textPrimary: '#333333',
  textSecondary: '#545759',
  textTertiary: '#8C8C8C',
  borderDefault: '#EBECED',
  radiusPanel: 10,
  radiusCard: 6,
  radiusControl: 4,
  pagePadding: 24,
  blockGap: 16
}
```

## Page-level component mapping

| Scenario | Recommended Ant Design components |
|---|---|
| top navigation | `Layout.Header` + `Menu` + `Dropdown` + `Avatar` |
| left navigation | `Layout.Sider` + `Menu` |
| org tree | `Tree` / `TreeSelect` |
| filter bar | `Form` + `Input` + `Select` + `DatePicker` + `Button` |
| time switching | `Tabs` / `Segmented` |
| KPI cards | `Card` + `Statistic` |
| chart cards | `Card` + chart container |
| list pages | `Table` + `Pagination` |
| config pages | `Form` + `InputNumber` + `Select` + `Tooltip` + `Upload` |
| empty state | `Empty` |
| loading state | `Spin` / `Skeleton` |
| feedback | `Alert` / `Message` / `Notification` |
| overlay | `Drawer` / `Modal` |

## Component notes

### Buttons
- primary action: `type="primary"`
- secondary action: default button
- dangerous action: `danger`
- typical height: 32px
- typical radius: 4px

### Cards
- normal cards: 6px radius
- highlighted / major panels: 10px radius
- typical internal padding: 16~24px

### Inputs
- keep Input / Select / DatePicker / InputNumber heights aligned
- placeholder uses tertiary text color
- tooltip is for compact explanation, not long-form documentation

### Tables
- default body text: 14px
- action column often fixed right when necessary
- bulk actions belong above the table
