# React 常用代码片段

> 创建日期：2026-05-25
> 分类：前端开发 / React
> 归属：full-stack-architect技能

---

## 1. 基础组件

### 1.1 函数组件基础

```tsx
import React from 'react';

interface Props {
  title: string;
  children?: React.ReactNode;
}

export default function BasicComponent({ title, children }: Props) {
  return (
    <div>
      <h1>{title}</h1>
      {children}
    </div>
  );
}
```

### 1.2 TypeScript组件完整示例

```tsx
import React, { useState, useCallback, useMemo } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserCardProps {
  user: User;
  onSelect?: (user: User) => void;
  isSelected?: boolean;
}

export const UserCard: React.FC<UserCardProps> = ({
  user,
  onSelect,
  isSelected = false,
}) => {
  const handleClick = useCallback(() => {
    onSelect?.(user);
  }, [user, onSelect]);

  const displayName = useMemo(() => {
    return user.name || 'Anonymous';
  }, [user.name]);

  return (
    <div
      onClick={handleClick}
      className={`p-4 rounded-lg cursor-pointer transition-colors ${
        isSelected 
          ? 'bg-blue-50 border-blue-200' 
          : 'bg-white border-gray-200'
      }`}
    >
      <h3 className="font-semibold">{displayName}</h3>
      <p className="text-sm text-gray-600">{user.email}</p>
    </div>
  );
};
```

---

## 2. State 管理

### 2.1 简单状态

```tsx
import React, { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  const increment = () => setCount(prev => prev + 1);
  const decrement = () => setCount(prev => prev - 1);
  const reset = () => setCount(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}
```

### 2.2 复杂对象状态

```tsx
import React, { useState } from 'react';

interface FormData {
  name: string;
  email: string;
  preferences: {
    newsletter: boolean;
    notifications: boolean;
  };
}

export function UserForm() {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    preferences: {
      newsletter: false,
      notifications: true,
    },
  });

  const updateField = (field: keyof FormData, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const updateNestedField = (
    category: keyof FormData,
    field: string,
    value: any
  ) => {
    setFormData(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [field]: value,
      },
    }));
  };

  return (
    <form>
      <input
        type="text"
        value={formData.name}
        onChange={(e) => updateField('name', e.target.value)}
        placeholder="Name"
      />
      <input
        type="email"
        value={formData.email}
        onChange={(e) => updateField('email', e.target.value)}
        placeholder="Email"
      />
      <label>
        <input
          type="checkbox"
          checked={formData.preferences.newsletter}
          onChange={(e) => 
            updateNestedField('preferences', 'newsletter', e.target.checked)
          }
        />
        Newsletter
      </label>
    </form>
  );
}
```

---

## 3. Hooks 使用

### 3.1 useEffect 基础

```tsx
import React, { useState, useEffect } from 'react';

interface Data {
  id: string;
  content: string;
}

export function DataFetcher({ url }: { url: string }) {
  const [data, setData] = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('Fetch failed');
        
        const result = await response.json();
        if (isMounted) setData(result);
      } catch (err) {
        if (isMounted) setError(err instanceof Error ? err.message : 'Error');
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    fetchData();

    return () => {
      isMounted = false;
    };
  }, [url]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>No data</div>;

  return <div>{data.content}</div>;}
```

### 3.2 useCallback 优化

```tsx
import React, { useState, useCallback, useMemo } from 'react';

interface Item {
  id: number;
  name: string;
}

export function ItemList() {
  const [items, setItems] = useState<Item[]>([]);
  const [filter, setFilter] = useState('');

  const addItem = useCallback((name: string) => {
    const newItem: Item = {
      id: Date.now(),
      name,
    };
    setItems(prev => [...prev, newItem]);
  }, []);

  const removeItem = useCallback((id: number) => {
    setItems(prev => prev.filter(item => item.id !== id));
  }, []);

  const filteredItems = useMemo(() => {
    return items.filter(item =>
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [items, filter]);

  return (
    <div>
      <input
        type="text"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Filter items..."
      />
      <ItemAdder onAdd={addItem} />
      <ul>
        {filteredItems.map(item => (
          <Item
            key={item.id}
            item={item}
            onRemove={removeItem}
          />
        ))}
      </ul>
    </div>
  );
}

interface ItemProps {
  item: Item;
  onRemove: (id: number) => void;
}

const Item = React.memo(({ item, onRemove }: ItemProps) => {
  console.log('Rendering item:', item.id);
  return (
    <li>
      {item.name}
      <button onClick={() => onRemove(item.id)}>Remove</button>
    </li>
  );
});

interface ItemAdderProps {
  onAdd: (name: string) => void;
}

const ItemAdder = React.memo(({ onAdd }: ItemAdderProps) => {
  const [name, setName] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      onAdd(name);
      setName('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Add item..."
      />
      <button type="submit">Add</button>
    </form>
  );
});
```

---

## 4. Context API

### 4.1 创建 Context

```tsx
import React, { createContext, useContext, useState, useCallback } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = useCallback((userData: User) => {
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    setUser(null);
  }, []);

  const value = {
    user,
    isAuthenticated: !!user,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
```

### 4.2 使用 Context

```tsx
import React from 'react';
import { useAuth } from './auth-context';

export function UserProfile() {
  const { user, isAuthenticated, logout } = useAuth();

  if (!isAuthenticated) {
    return <div>Please log in</div>;
  }

  return (
    <div>
      <h1>Welcome, {user.name}</h1>
      <p>Email: {user.email}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

---

## 5. 表单处理

### 5.1 受控表单

```tsx
import React, { useState } from 'react';

interface LoginFormData {
  email: string;
  password: string;
  remember: boolean;
}

export function LoginForm() {
  const [formData, setFormData] = useState<LoginFormData>({
    email: '',
    password: '',
    remember: false,
  });
  const [errors, setErrors] = useState<Partial<LoginFormData>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = () => {
    const newErrors: Partial<LoginFormData> = {};
    
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.password) newErrors.password = 'Password is required';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validate()) return;
    
    setIsSubmitting(true);
    
    try {
      // Submit logic here
      console.log('Form submitted:', formData);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          disabled={isSubmitting}
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          disabled={isSubmitting}
        />
        {errors.password && <span className="error">{errors.password}</span>}
      </div>

      <div>
        <label>
          <input
            name="remember"
            type="checkbox"
            checked={formData.remember}
            onChange={handleChange}
            disabled={isSubmitting}
          />
          Remember me
        </label>      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

---

## 6. 组件模式

### 6.1 复合组件模式

```tsx
import React, { createContext, useContext, useState } from 'react';

interface TabsContextType {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextType | undefined>(undefined);

interface TabsProps {
  defaultTab?: string;
  children: React.ReactNode;
}

export function Tabs({ defaultTab, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab || '');

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

interface TabListProps {
  children: React.ReactNode;
}

export function TabList({ children }: TabListProps) {
  return <div className="tab-list">{children}</div>;
}

interface TabProps {
  id: string;
  children: React.ReactNode;
}

export function Tab({ id, children }: TabProps) {
  const { activeTab, setActiveTab } = useTabsContext();
  const isActive = activeTab === id;

  return (
    <button
      className={`tab ${isActive ? 'active' : ''}`}
      onClick={() => setActiveTab(id)}
    >
      {children}
    </button>
  );
}

interface TabPanelsProps {
  children: React.ReactNode;
}

export function TabPanels({ children }: TabPanelsProps) {
  return <div className="tab-panels">{children}</div>;
}

interface TabPanelProps {
  id: string;
  children: React.ReactNode;
}

export function TabPanel({ id, children }: TabPanelProps) {
  const { activeTab } = useTabsContext();
  
  if (activeTab !== id) return null;
  
  return <div className="tab-panel">{children}</div>;
}

function useTabsContext() {
  const context = useContext(TabsContext);
  if (context === undefined) {
    throw new Error('Tabs components must be used within a Tabs provider');
  }
  return context;
}
```

### 6.2 使用复合组件

```tsx
import React from 'react';
import { Tabs, TabList, Tab, TabPanels, TabPanel } from './tabs';

export function ExampleTabs() {
  return (
    <Tabs defaultTab="home">
      <TabList>
        <Tab id="home">Home</Tab>
        <Tab id="profile">Profile</Tab>
        <Tab id="settings">Settings</Tab>
      </TabList>
      
      <TabPanels>
        <TabPanel id="home">
          <h1>Home</h1>
          <p>Welcome home!</p>
        </TabPanel>
        
        <TabPanel id="profile">
          <h1>Profile</h1>
          <p>Your profile</p>
        </TabPanel>
        
        <TabPanel id="settings">
          <h1>Settings</h1>
          <p>Your settings</p>
        </TabPanel>
      </TabPanels>
    </Tabs>
  );
}
```

---

## 7. 性能优化

### 7.1 React.memo

```tsx
import React, { memo } from 'react';

interface ExpensiveComponentProps {
  data: string[];
  onItemClick: (item: string) => void;
}

export const ExpensiveComponent = memo(({
  data,
  onItemClick,
}: ExpensiveComponentProps) => {
  console.log('ExpensiveComponent rendered');
  
  return (
    <ul>
      {data.map((item, index) => (
        <li key={index} onClick={() => onItemClick(item)}>
          {item}
        </li>
      ))}
    </ul>
  );
}, (prevProps, nextProps) => {
  // Custom comparison function
  return (
    prevProps.data === nextProps.data &&
    prevProps.onItemClick === nextProps.onItemClick
  );
});
```

---

## 使用说明

这些代码片段可以直接复制使用，根据具体需求进行调整。建议在实际项目中：

1. 根据项目规范调整样式
2. 添加适当的错误处理
3. 完善TypeScript类型定义
4. 添加必要的注释说明

