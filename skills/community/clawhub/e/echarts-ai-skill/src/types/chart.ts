export type ChartType =
  | "line"
  | "bar"
  | "pie"
  | "scatter"
  | "effectScatter"
  | "radar"
  | "funnel"
  | "gauge"
  | "heatmap"
  | "treemap"
  | "sunburst"
  | "sankey"
  | "graph"
  | "candlestick"
  | "boxplot"
  | "parallel"
  | "map"
  | "lines";

export type ChartGoal = "trend" | "comparison" | "composition" | "distribution" | "relationship" | "flow" | "unknown";

export type Primitive = string | number | boolean | null;

export type DataRow = Record<string, Primitive>;

export type ChartOption = Record<string, unknown>;
export type ChartSeriesOption = Record<string, unknown>;

export interface ChartSeriesInput {
  name: string;
  field: string;
}

export interface ChartIndicator {
  name: string;
  max?: number;
  min?: number;
}

export interface ChartNode {
  name: string;
  value?: number;
  category?: string | number;
  symbolSize?: number;
  x?: number;
  y?: number;
  children?: ChartNode[];
}

export interface ChartLink {
  source: string;
  target: string;
  value?: number;
}

export interface ChartLinePoint {
  coords: Array<[number, number]>;
  value?: number;
  fromName?: string;
  toName?: string;
}

export interface ChartParallelAxis {
  dim: number;
  name: string;
  min?: number;
  max?: number;
}

export interface ChartRequest {
  title?: string;
  subtitle?: string;
  description?: string;
  chartType?: ChartType;
  goal?: ChartGoal;
  dataset: DataRow[];
  categoryField?: string;
  xField?: string;
  yField?: string;
  valueField?: string;
  groupField?: string;
  series?: ChartSeriesInput[];
  indicators?: ChartIndicator[];
  nodes?: ChartNode[];
  links?: ChartLink[];
  tree?: ChartNode[];
  lineCoordinates?: ChartLinePoint[];
  mapName?: string;
  dimensions?: string[];
  parallelAxis?: ChartParallelAxis[];
  openField?: string;
  closeField?: string;
  lowField?: string;
  highField?: string;
  minField?: string;
  q1Field?: string;
  medianField?: string;
  q3Field?: string;
  maxField?: string;
  width?: number;
  height?: number;
  rawOption?: ChartOption;
}

export interface ChartField {
  name: string;
  type: "number" | "string" | "boolean" | "date" | "unknown";
}

export interface ChartSpec {
  title?: string;
  subtitle?: string;
  chartType: ChartType;
  goal: ChartGoal;
  dataset: DataRow[];
  categoryField?: string;
  xField?: string;
  yField?: string;
  valueField?: string;
  groupField?: string;
  series: ChartSeriesInput[];
  indicators: ChartIndicator[];
  nodes: ChartNode[];
  links: ChartLink[];
  tree: ChartNode[];
  lineCoordinates: ChartLinePoint[];
  mapName?: string;
  dimensions: string[];
  parallelAxis: ChartParallelAxis[];
  openField?: string;
  closeField?: string;
  lowField?: string;
  highField?: string;
  minField?: string;
  q1Field?: string;
  medianField?: string;
  q3Field?: string;
  maxField?: string;
  width: number;
  height: number;
  fields: ChartField[];
  rawOption?: ChartOption;
}
