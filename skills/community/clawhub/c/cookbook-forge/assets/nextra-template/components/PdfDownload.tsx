export default function PdfDownload({ href, label }: { href: string; label: string }) {
  return (
    <a className="download-btn" href={href} download>⬇️ {label}</a>
  )
}
