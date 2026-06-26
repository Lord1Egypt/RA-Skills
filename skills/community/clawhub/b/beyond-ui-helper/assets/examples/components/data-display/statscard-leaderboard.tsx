import { StatsCard, Badge, Button } from '@beyondcorp/beyond-ui';
import '@beyondcorp/beyond-ui/dist/styles.css';
import { Zap, TrendingUp } from 'lucide-react';

export function LeaderboardHighlight() {
  return (
    <StatsCard
      title="Revenue leader"
      value="$84,500"
      helperText="Acme Analytics"
      trendLabel="vs previous 30 days"
      trendValue="15%"
      icon={<Zap className="h-5 w-5" />}
    >
      <div className="flex items-center justify-between pt-4">
        <Badge variant="success" className="gap-1">
          <TrendingUp className="h-4 w-4" />
          1st place
        </Badge>
        <Button variant="ghost" size="sm">
          View details
        </Button>
      </div>
    </StatsCard>
  );
}
