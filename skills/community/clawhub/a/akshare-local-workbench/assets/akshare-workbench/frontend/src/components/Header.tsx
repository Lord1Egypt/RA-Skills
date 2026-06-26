interface HeaderProps {
  sectorCount: number;
  indicatorCount: number;
}

export function Header({ sectorCount, indicatorCount }: HeaderProps) {
  return (
    <header className="site-header">
      <div className="global-notice">
        <span className="global-notice-icon">⚠️</span>
        考虑到 AKShare 及数据供应商 API 并发限制，请手动点击「刷新」加载实时数据。
      </div>
      <div className="site-header-inner">
        <div className="brand">
          <span className="brand-name">AKShare 调用工具</span>
        </div>
        <div className="header-meta">
          <span className="meta-pill">
            <span className="meta-value">{sectorCount}</span>个板块
          </span>
          <span className="meta-pill">
            <span className="meta-value">{indicatorCount}</span>个指标
          </span>
        </div>
      </div>
    </header>
  );
}
