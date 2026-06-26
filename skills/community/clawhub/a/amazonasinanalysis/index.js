async function executeSkill(input, context) {
  try {
    const baseUrl = process.env.NOVAI360_API_URL || 'https://api.novai360.com';
    const apiUrl = `${baseUrl}/chat`;
    
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: input,
        context: context
      })
    });

    const data = await response.json();
    if (data.success) {
      return {
        success: true,
        result: data.response,
        intent: data.intent,
        data: data.data
      };
    } else {
      return {
        success: false,
        error: data.error || 'API 调用失败'
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message || 'API 调用失败'
    };
  }
}

async function getSkills() {
  try {
    const baseUrl = process.env.NOVAI360_API_URL || 'https://api.novai360.com';
    const apiUrl = `${baseUrl}/skills`;
    const response = await fetch(apiUrl);
    const data = await response.json();
    return data;
  } catch (error) {
    return { success: false, error: error.message };
  }
}

module.exports = {
  execute: executeSkill,
  getSkills: getSkills
};