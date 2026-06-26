import React from 'react';
import {
  DataTable,
  Badge,
  Button,
  Avatar,
  AvatarImage,
  AvatarFallback,
} from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { Eye, Edit, Trash2 } from 'lucide-react';

type User = {
  id: number;
  name: string;
  email: string;
  role: string;
  status: 'active' | 'inactive' | 'pending';
  avatar: string;
  joinDate: string;
};

const users: User[] = [
  {
    id: 1,
    name: 'Jane Cooper',
    email: 'jane@acme.co',
    role: 'Design Lead',
    status: 'active',
    avatar: 'https://i.pravatar.cc/64?img=1',
    joinDate: '2024-01-09',
  },
  {
    id: 2,
    name: 'Cody Fisher',
    email: 'cody@acme.co',
    role: 'Product Manager',
    status: 'pending',
    avatar: 'https://i.pravatar.cc/64?img=8',
    joinDate: '2024-02-18',
  },
  {
    id: 3,
    name: 'Courtney Henry',
    email: 'courtney@acme.co',
    role: 'Engineer',
    status: 'inactive',
    avatar: 'https://i.pravatar.cc/64?img=5',
    joinDate: '2023-11-03',
  },
];

const columns = [
  {
    key: 'user',
    title: 'Member',
    dataIndex: 'name' as const,
    sortable: true,
    render: (_name: string, record: User) => (
      <div className="flex items-center gap-3">
        <Avatar size="sm">
          <AvatarImage src={record.avatar} />
          <AvatarFallback>{record.name.split(' ').map((n) => n[0]).join('')}</AvatarFallback>
        </Avatar>
        <div>
          <p className="text-sm font-medium text-secondary-900">{record.name}</p>
          <p className="text-xs text-secondary-500">{record.email}</p>
        </div>
      </div>
    ),
  },
  {
    key: 'role',
    title: 'Role',
    dataIndex: 'role' as const,
    sortable: true,
    filterable: true,
    filterType: 'select' as const,
    filterOptions: [
      { label: 'Design Lead', value: 'Design Lead' },
      { label: 'Product Manager', value: 'Product Manager' },
      { label: 'Engineer', value: 'Engineer' },
    ],
  },
  {
    key: 'status',
    title: 'Status',
    dataIndex: 'status' as const,
    filterable: true,
    filterType: 'select' as const,
    filterOptions: [
      { label: 'Active', value: 'active' },
      { label: 'Inactive', value: 'inactive' },
      { label: 'Pending', value: 'pending' },
    ],
    render: (status: User['status']) => (
      <Badge
        variant={
          status === 'active'
            ? 'success'
            : status === 'pending'
            ? 'warning'
            : 'secondary'
        }
      >
        {status}
      </Badge>
    ),
  },
  {
    key: 'joinDate',
    title: 'Joined',
    dataIndex: 'joinDate' as const,
    sortable: true,
  },
  {
    key: 'actions',
    title: 'Actions',
    dataIndex: 'id' as const,
    align: 'center' as const,
    render: (_id: number, record: User) => (
      <div className="flex items-center justify-center gap-1">
        <Button variant="ghost" size="sm" aria-label={`View ${record.name}`}>
          <Eye className="h-4 w-4" />
        </Button>
        <Button variant="ghost" size="sm" aria-label={`Edit ${record.name}`}>
          <Edit className="h-4 w-4" />
        </Button>
        <Button variant="ghost" size="sm" aria-label={`Deactivate ${record.name}`}>
          <Trash2 className="h-4 w-4 text-danger-600" />
        </Button>
      </div>
    ),
  },
];

export function UsersTable() {
  return (
    <DataTable<User>
      columns={columns}
      dataSource={users}
      rowKey="id"
      pagination={{ current: 1, total: users.length, pageSize: 10 }}
      rowSelection={{
        type: 'checkbox',
        onChange: (selectedRowKeys, selectedRows) => {
          console.log('Selected rows', selectedRowKeys, selectedRows);
        },
      }}
    />
  );
}
