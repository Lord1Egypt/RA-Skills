const hospital = require('../data/hospital.json')
const { render, loadI18n } = require('./renderer')

async function getBookingGuide(lang = 'zh') {
  return render(hospital, lang)
}

function getHospital() {
  return { ...hospital }
}

module.exports = { getBookingGuide, getHospital }
