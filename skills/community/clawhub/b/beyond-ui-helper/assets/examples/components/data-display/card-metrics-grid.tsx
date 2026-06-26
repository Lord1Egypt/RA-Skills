import { Card, CardHeader, CardTitle, CardDescription, CardContent, Badge } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { TrendingUp, TrendingDown, Users, DollarSign } from 'lucide-react';

const metrics = [
  {
    title: 'Monthly Recurring Revenue',
    value: '$128,400',
    delta: '+12.4% vs last month',
    trend: 'up',
    icon: DollarSign,
  },
  {
    title: 'Active customers',
    value: '6,892',
    delta: '+320 new this week',
    trend: 'up',
    icon: Users,
  },
  {
    title: 'Churn rate',
    value: '2.6%',
    delta: '+0.4% vs target',
    trend: 'down',
    icon: TrendingDown,
  },
];

export function MetricsGrid() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {metrics.map(({ title, value, delta, trend, icon: Icon }) => (
        <Card key={title} className="border border-secondary-100">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-secondary-600">{title}</CardTitle>
            <span className="rounded-lg bg-primary-50 p-2 text-primary-600">
              <Icon className="h-4 w-4" />
            </span>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-semibold text-secondary-900">{value}</div>
            <div className="flex items-center gap-2 pt-2 text-xs text-secondary-500">
              {trend === 'up' ? (
                <Badge variant="success" className="gap-1">
                  <TrendingUp className="h-3 w-3" />
                  {delta}
                </Badge>
              ) : (
                <Badge variant="danger" className="gap-1">
                  <TrendingDown className="h-3 w-3" />
                  {delta}
                </Badge>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
