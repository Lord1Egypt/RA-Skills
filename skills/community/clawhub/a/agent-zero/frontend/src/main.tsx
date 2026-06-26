import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import App from './App.tsx'
import { PropertyDetail } from './PropertyDetail.tsx'
import { ManageSearchProfiles } from './ManageSearchProfiles.tsx'
import { InboxPage } from './InboxPage.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/property/:id" element={<PropertyDetail />} />
        <Route path="/search-profiles" element={<ManageSearchProfiles />} />
        <Route path="/inbox" element={<InboxPage />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
