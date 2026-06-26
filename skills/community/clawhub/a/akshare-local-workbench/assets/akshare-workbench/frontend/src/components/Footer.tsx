export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="site-footer">
      <div className="footer-inner">
        <div className="footer-top">
          <div className="footer-brand">
            <span className="footer-brand-name">AKShare 调用工具</span>
            <span className="footer-tagline">金融数据爱好者的交流与学习工作台 · 非商业用途</span>
          </div>
          <div className="footer-links">
            <a className="footer-pill" href="mailto:davidtian@outlook.com">
              <span className="footer-pill-label">交流学习</span>
              davidtian@outlook.com
            </a>
            <a
              className="footer-pill"
              href="https://akshare.akfamily.xyz/"
              target="_blank"
              rel="noreferrer"
            >
              <span className="footer-pill-label">数据来源</span>
              AKShare
            </a>
          </div>
        </div>

        <div className="footer-notes">
          <div className="footer-note">
            <span className="footer-note-title">使用须知</span>
            <p>
              本工具仅供金融数据爱好者<strong>交流与学习</strong>，
              <strong>禁止用于任何商业用途</strong>。数据来自 AKShare 及其原始数据供应商，
              使用时请务必遵守 AKShare 开源协议与各数据源的使用条款，避免高频抓取等违规行为。
            </p>
          </div>
          <div className="footer-note">
            <span className="footer-note-title">免责声明</span>
            <p>
              本工具不对数据的准确性、完整性、及时性作任何保证，所有内容
              <strong>不构成任何投资建议</strong>。任何人据此操作所产生的风险与损失，
              均由使用者自行承担，本工具及作者概不负责。一旦使用即视为已知悉并同意本声明。
            </p>
          </div>
          <div className="footer-note">
            <span className="footer-note-title">开源许可</span>
            <p>
              本工具基于开源财经数据接口库{" "}
              <a
                className="footer-inline-link"
                href="https://github.com/akfamily/akshare/blob/main/LICENSE"
                target="_blank"
                rel="noreferrer"
              >
                AKShare
              </a>{" "}
              构建，AKShare 以 <strong>MIT License</strong> 发布
              （Copyright © 2019-2026 Albert King）。本项目遵循同样的 MIT 协议，
              在再分发时保留上述版权与许可声明；AKShare 按“原样”提供，不附带任何明示或默示担保。
            </p>
          </div>
        </div>

        <div className="footer-bottom">
          <span>© {year} AKShare 调用工具</span>
          <span className="footer-bottom-sep">·</span>
          <span>基于 AKShare（MIT License）构建</span>
          <span className="footer-bottom-sep">·</span>
          <span>Made for learning, not for trading.</span>
        </div>
      </div>
    </footer>
  );
}
