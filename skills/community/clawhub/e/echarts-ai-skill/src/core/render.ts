import type { ChartOption } from "../types/chart.js";

const CDN_URL = "https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js";

export function renderHtml(option: ChartOption, width: number, height: number): string {
  const optionJson = JSON.stringify(option, null, 2);
  return `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ECharts Preview</title>
    <script src="${CDN_URL}"></script>
    <style>
      html, body { margin: 0; padding: 0; background: #f3f5f7; font-family: "Segoe UI", sans-serif; }
      .wrap { padding: 24px; }
      #chart { width: ${width}px; height: ${height}px; margin: 0 auto; background: #fff; border-radius: 16px; box-shadow: 0 12px 40px rgba(15, 23, 42, 0.10); }
    </style>
  </head>
  <body>
    <div class="wrap">
      <div id="chart"></div>
    </div>
    <script>
      const chart = echarts.init(document.getElementById("chart"));
      const option = ${optionJson};
      chart.setOption(option);
    </script>
  </body>
</html>`;
}

export async function renderSvg(option: ChartOption, width: number, height: number): Promise<string> {
  const echarts = await import("echarts");
  const chart = echarts.init(null, undefined, {
    renderer: "svg",
    ssr: true,
    width,
    height
  });
  chart.setOption(option as any);
  const svg = chart.renderToSVGString();
  chart.dispose();
  return svg;
}
