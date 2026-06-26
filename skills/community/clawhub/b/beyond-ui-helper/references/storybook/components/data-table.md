# DataTable

## Usage
```tsx
import { DataTable } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';

const columns = [
  {
    key: 'name',
    title: 'Name',
    dataIndex: 'name',
    sortable: true,
    filterable: true,
  },
  {
    key: 'role',
    title: 'Role',
    dataIndex: 'role',
  },
];

const users = [
  { id: 1, name: 'Avery Howard', role: 'Designer' },
  { id: 2, name: 'Diego Mendez', role: 'Engineer' },
];

export function UsersTable() {
  return (
    <DataTable
      columns={columns}
      dataSource={users}
      rowKey="id"
      pagination={{ current: 1, total: users.length, pageSize: 10 }}
    />
  );
}
```

## Props
| Prop | Type | Description |
|------|------|-------------|
| columns | Column<T>[] | Column definitions (title, dataIndex, filters, custom renderers) |
| dataSource | T[] | Array of data records |
| rowKey | string | Unique key for each row |
| pagination | { current: number; pageSize: number; total: number; ... } | Pagination controls (set to `false` to hide) |
| size | 'small' | 'middle' | 'large' | Adjusts padding and typography (default: middle) |
| bordered | boolean | Adds borders around table and cells |
| rowSelection | { type?: 'checkbox' | 'radio'; onChange?: Function; ... } | Enables row selection |
| loading | boolean | Displays loading spinner |

## Notes
- Columns support custom renderers for avatars, action cells, etc.
- On mobile (sm down), the table renders as stacked cards for readability.
- Compose filters and search inputs outside the table for custom toolbars.

Story source: stories/DataTable.stories.tsx
