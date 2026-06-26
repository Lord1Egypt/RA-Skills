import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL || 'https://wxwuziwpfagqxocjvhti.supabase.co';
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseKey) {
  console.log('❌ Missing SUPABASE_SERVICE_ROLE_KEY');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function getTestAgent() {
  const { data, error } = await supabase
    .from('bloom_agents')
    .select('agent_user_id, identity_data')
    .order('created_at', { ascending: false })
    .limit(1)
    .single();

  if (error || !data) {
    console.log('❌ No agents found:', error?.message);
    process.exit(1);
  }

  console.log('✅ Found test agent:\n');
  console.log('🎴 Agent User ID:', data.agent_user_id);
  console.log('🔗 Local Test URL: http://localhost:3000/agents/' + data.agent_user_id);
  console.log('\n🧪 Test Steps:');
  console.log('   1. Open the URL above');
  console.log('   2. Click "Save My Card" button');
  console.log('   3. Verify email capture modal appears');
  console.log('   4. Submit a test email');
  console.log('   5. Check success message: "Check your email! 📧"\n');
}

getTestAgent();
